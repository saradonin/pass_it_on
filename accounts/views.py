from datetime import timedelta
import uuid
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView, CreateView, UpdateView, ListView

from accounts.models import User, Token
from accounts.validators import validate_last_admin, validate_password, validate_user_data, validate_email_unique
from donations.models import Donation, Institution


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Custom mixin testing is user is staff
    """

    def test_func(self):
        return self.request.user.is_staff


class UserLoginView(View):
    """
    View for user login.
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')

        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('register')
        elif user.is_active is False:
            ctx = {
                'message': "Twoje konto nie zostało aktywowane. Sprawdź email."
            }
            return render(request, 'message.html', ctx)
        else:
            login(request, user)
            return redirect('index')


class UserLogoutView(LoginRequiredMixin, View):
    """
    View for user logout.
    """
    login_url = "/login/"

    def get(self, request):
        logout(request)
        return redirect('index')


class UserRegisterView(View):
    """
    View for registering new user.
    """

    def get(self, request):
        return render(request, 'user_register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # validation
        user_data_errors = validate_user_data(name, surname, email)
        user_unique_errors = validate_email_unique(email)
        password_errors = validate_password(password, password2)
        ctx = {**user_data_errors, **user_unique_errors, **password_errors}

        if not ctx:
            confirmation_token = str(uuid.uuid4())
            user = User.objects.create_user(
                username=email,
                first_name=name,
                last_name=surname,
                email=email,
                password=password,
                is_active=False,
            )
            Token.objects.create(user=user, token=confirmation_token)

            # sending email
            confirmation_link = f"{settings.BASE_URL}/confirm/{confirmation_token}"
            email_subject = "Aktywacja konta"
            email_message = f"Cześć {user.first_name}, \n Kliknij poniższy link aby dokończyć rejestrację \n {confirmation_link}"
            send_mail(email_subject, email_message,
                      settings.EMAIL_HOST_USER, [email])

            ctx = {
                'message': "Dziękujemy za rejestrację konta. Na wskazany adres email został wysłany link aktywacyjny."
            }
            return render(request, 'message.html', ctx)

        return render(request, 'user_register.html', ctx)


class UserConfirmRegistrationView(View):
    """
    View for confirming registration
    """

    def get(self, request, token):
        logout(request)
        try:
            token_instance = Token.objects.get(token=token)
            one_day_ago = timezone.now() - timedelta(days=1)
            user = token_instance.user

            if token_instance.date_created < one_day_ago:
                if user.is_active is False and user.date_joined == token_instance.date_created:
                    user.delete()

                token_instance.delete()
                ctx = {
                    'message': "Link aktywacyjny wygasł. Prosimy o ponowną rejestrację."
                }
            else:
                user.is_active = True
                token_instance.delete()
                user.save()
                ctx = {
                    'message': "Twoje konto zostało aktywowane. Możesz się teraz zalogować."
                }
        except Token.DoesNotExist:
            ctx = {
                'message': "Link aktywacyjny jest nieprawidłowy lub został już wykorzystany"
            }
        return render(request, 'message.html', ctx)


class UserSettingsView(LoginRequiredMixin, View):
    """
    View for displaying user settings.
    """

    def get(self, request):
        return render(request, 'user_settings.html')

    def post(self, request):
        user = request.user
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # validation
        ctx = validate_user_data(name, surname, email)
        if not password:
            ctx["password_msg"] = "Podaj hasło aby zapisać zmiany"
        elif not check_password(password, user.password):
            ctx["password_msg"] = "Podane hasło jest nieprawidłowe"

        if not ctx:
            user.first_name = name
            user.last_name = surname
            user.email = user.username = email
            user.save()
            return redirect('user-settings')

        return render(request, 'user_settings.html', ctx)


class UserPasswordSendEmailView(View):
    """
    View for sending password reset email
    """

    def get(self, request):
        return render(request, 'user_password_reset_email.html')

    def post(self, request):
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            ctx = {
                'message': "Konto powiązane z tym adresem email nie istnieje."
            }
            return render(request, 'user_password_reset_email.html', ctx)
        else:
            password_reset_token = str(uuid.uuid4())
            user = User.objects.get(email=email)
            Token.objects.create(user=user, token=password_reset_token)

            # sending email
            email_subject = "Odzyskiwanie hasła"
            reset_link = f"{settings.BASE_URL}/new-password/{password_reset_token}"
            email_message = f"Cześć {user.first_name}, \n Kliknij w poniższy link aby ustawić nowe hasło \n {reset_link}"

            send_mail(email_subject, email_message,
                      settings.EMAIL_HOST_USER, [email])

            ctx = {
                'message': "Na wskazany adres email wysłaliśmy link do zmiany hasła."
            }
            return render(request, 'message.html', ctx)


class UserPasswordResetView(View):
    """
    View for setting up new password
    """

    def get(self, request, token):
        try:
            token_instance = Token.objects.get(token=token)
            one_day_ago = timezone.now() - timedelta(days=1)

            if token_instance.date_created < one_day_ago:
                ctx = {
                    'message': "Link do zmiany hasła wygasł."
                }
                token_instance.delete()
                return render(request, 'message.html', ctx)
            return render(request, 'user_password_reset.html')

        except Token.DoesNotExist:
            ctx = {
                'message': "Link do zmiany hasła jest nieprawidłowy lub został już wykorzystany"
            }
            return render(request, 'message.html', ctx)

    def post(self, request, token):
        token_instance = Token.objects.get(token=token)
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        ctx = validate_password(new_password, new_password2)

        if not ctx:
            user = token_instance.user
            user.set_password(new_password)
            user.save()
            token_instance.delete()
            return redirect('login')
        return render(request, 'user_password_reset.html', ctx)


class UserPasswordChangeView(LoginRequiredMixin, View):
    """
    View for changing user password.
    """

    def get(self, request):
        return render(request, 'user_change_password.html')

    def post(self, request):
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        # validation
        ctx = validate_password(new_password, new_password2)
        if not old_password:
            ctx["old_password_msg"] = "Podaj swoje obecne hasło"
        elif not check_password(old_password, user.password):
            ctx["old_password_msg"] = "Podane hasło jest nieprawidłowe"

        if not ctx:
            user.set_password(new_password)
            user.save()
            return redirect('login')

        return render(request, 'user_change_password.html', ctx)


class UserProfileView(LoginRequiredMixin, View):
    """
    View for displaying user profile.
    """

    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(
            user=user).order_by("is_taken", "-pick_up_date")

        paginator = Paginator(donations, 20)
        # current page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        ctx = {
            'page_obj': page_obj,
        }
        return render(request, 'user_profile.html', ctx)


class AdminMenuView(StaffRequiredMixin, View):
    """
    View for rendering admin panel.
    """
    login_url = "/login/"

    def get(self, request):
        return render(request, 'admin_panel.html')


class UserListView(StaffRequiredMixin, ListView):
    """
    View for displaying a list of users.
    """
    model = User
    ordering = ['id']
    template_name = "user_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserAddView(StaffRequiredMixin, View):
    """
    View for registering new user.
    """

    def get(self, request):
        return render(request, 'user_add_form.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_active = bool(request.POST.get('is_active'))
        is_staff = bool(request.POST.get('is_staff'))

        # validation
        user_data_errors = validate_user_data(name, surname, email)
        user_unique_errors = validate_email_unique(email)
        password_errors = validate_password(password, password2)
        ctx = {**user_data_errors, **user_unique_errors, **password_errors}

        if not ctx:
            User.objects.create_user(
                username=email,
                first_name=name,
                last_name=surname,
                email=email,
                password=password,
                is_active=is_active,
                is_staff=is_staff,
            )
            return redirect('user-list')

        return render(request, 'user_add_form.html', ctx)


class UserUpdateView(StaffRequiredMixin, View):
    """
    View for updating user details.
    """

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        ctx = {
            "user": user
        }
        return render(request, 'user_update_form.html', ctx)

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        is_active = bool(request.POST.get('is_active'))
        is_staff = bool(request.POST.get('is_staff'))

        # validation
        ctx = validate_user_data(name, surname, email)

        if not ctx:
            user.first_name = name
            user.last_name = surname
            user.username = user.email = email
            user.is_active = is_active
            user.is_staff = is_staff
            user.save()
            return redirect('user-list')

        return render(request, 'user_update_form.html', ctx)


class UserDeleteView(StaffRequiredMixin, View):
    """
    Display confirmation and handle delete user
    """

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)

        ctx = validate_last_admin(request, user)
        ctx["user"] = user
        return render(request, 'user_confirm_delete.html', ctx)

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        ctx = validate_last_admin(request, user)

        if not ctx:
            user.delete()
            return redirect('user-list')


class InstitutionListView(StaffRequiredMixin, ListView):
    """
    View for displaying a list of institutions.
    """
    model = Institution
    ordering = ['id']
    template_name = "institution_list.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class InstitutionAddView(StaffRequiredMixin, CreateView):
    """
    View for adding new institution.
    """
    model = Institution
    fields = "__all__"
    template_name = "institution_add_form.html"
    success_url = reverse_lazy('institution-list')


class InstitutionUpdateView(StaffRequiredMixin, UpdateView):
    """
    View for updating institution details.
    """
    model = Institution
    fields = "__all__"
    template_name = "institution_update_form.html"
    success_url = reverse_lazy('institution-list')


class InstitutionDeleteView(StaffRequiredMixin, DeleteView):
    """
    Display confirmation and handle delete institution
    """
    model = Institution
    template_name = 'institution_confirm_delete.html'
    pk_url_kwarg = 'institution_id'
    success_url = reverse_lazy('institution-list')


class ContactFormView(View):
    """
    View for handling contact form.
    """

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        message = request.POST.get('message')

        if name and surname and message:
            email_subject = f"Wiadomość od {name} {surname}"
            email_message = f"{name} {surname} przesłał wiadomość o następującej treści: \n {message}"
            email_list = [
                user.email for user in User.objects.filter(is_staff=True)]

            send_mail(email_subject, email_message,
                      settings.EMAIL_HOST_USER, email_list)

            ctx = {
                'message': "Twoja wiadomość została wysłana. Dziękujemy za kontakt."
            }
            return render(request, 'message.html', ctx)
