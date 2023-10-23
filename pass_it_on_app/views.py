from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from pass_it_on_app.models import Institution, Donation, User, Category


class IndexView(View):
    """
    View for rendering the index page.
    """

    def get(self, request):
        bags_given_count = 0
        institutions_supported = []
        for donation in Donation.objects.all():
            bags_given_count += donation.quantity

            if donation.institution.id not in institutions_supported:
                institutions_supported.append(donation.institution.id)

        foundations = Institution.objects.filter(type="1").order_by("name")
        non_gov_organizations = Institution.objects.filter(type="2").order_by("name")
        local_collections = Institution.objects.filter(type="3").order_by("name")

        ctx = {
            "institutions_supported": len(institutions_supported),
            "bags_given": bags_given_count,
            "foundations": foundations,
            "non_gov_organizations": non_gov_organizations,
            "local_collections": local_collections,
        }
        return render(request, 'index.html', ctx)


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

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('register')


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
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # validation
        ctx = {}
        if not name:
            ctx["name_msg"] = "Podaj imię"
        if not surname:
            ctx["surname_msg"] = "Podaj nazwisko"
        if not email:
            ctx["email_msg"] = "Podaj email"
        if not password:
            ctx["password_msg"] = "Podaj hasło"
        elif len(password) < 8:
            ctx["password_msg"] = "Hasło musi zawierać co najmniej 8 znaków"
        if not password2 or password != password2:
            ctx["password2_msg"] = "Hasła muszą być takie same"

        if name and surname and email and password and password2:
            User.objects.create_user(
                username=email,
                first_name=name,
                last_name=surname,
                email=email,
                password=password
            )
            return redirect('login')

        return render(request, 'register.html', ctx)


class DonationAddView(LoginRequiredMixin, View):
    """
    View for rendering the donation form.
    """
    login_url = "/login/"

    def get(self, request):
        ctx = {
            'categories': Category.objects.all().order_by('name'),
            'institutions': Institution.objects.all().order_by('name')
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        user = request.user
        categories = request.POST.getlist('categories')  # Get selected category IDs
        quantity = request.POST.get('bags')  # Get bags quantity
        institution_name = request.POST.get('organization')  # Get selected institution name
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')

        selected_categories = Category.objects.filter(id__in=categories)
        institution = Institution.objects.get(name=institution_name)

        if quantity and categories and institution and address and phone_number and city and postcode and pick_up_date and pick_up_time:
            # Create a Donation object with the form data
            donation = Donation.objects.create(
                quantity=quantity,
                institution=institution,
                address=address,
                city=city,
                zip_code=postcode,
                phone_number=phone_number,
                pick_up_date=pick_up_date,
                pick_up_time=pick_up_time,
                pick_up_comment=pick_up_comment,
                user=user
            )
            donation.categories.set(selected_categories)
            return redirect('donation-confirmation')

        ctx = {
            'categories': Category.objects.all().order_by('name'),
            'institutions': Institution.objects.all().order_by('name')
        }
        return render(request, 'form.html', ctx)


class DonationConfirmView(LoginRequiredMixin, View):
    """
    View for rendering the donation confirmation message.
    """
    login_url = "/login/"

    def get(self, request):
        return render(request, 'form-confirmation.html')


class DonationConfirmReceivedView(LoginRequiredMixin, View):
    """
    View for confirming the receiving of a donation.
    """
    def get(self, request, donation_id):
        ctx = {
            "donation": Donation.objects.get(id=donation_id)
        }
        return render(request, 'donation_confirm_received.html', ctx)

    def post(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect('user-profile')


class DonationDetailsView(LoginRequiredMixin, View):
    """
    View for displaying the donation details
    """
    def get(self, request, donation_id):
        ctx = {
            'donation': Donation.objects.get(id=donation_id)
        }
        return render(request, 'donation_details.html', ctx)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Custom mixin testing is user is staff
    """

    def test_func(self):
        return self.request.user.is_staff


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
        is_active = True if request.POST.get('is_active') else False
        is_staff = True if request.POST.get('is_staff') else False

        # validation
        ctx = {}
        if not name:
            ctx["name_msg"] = "Podaj imię"
        if not surname:
            ctx["surname_msg"] = "Podaj nazwisko"
        if not email:
            ctx["email_msg"] = "Podaj email"
        if not password:
            ctx["password_msg"] = "Podaj hasło"
        elif len(password) < 8:
            ctx["password_msg"] = "Hasło musi zawierać co najmniej 8 znaków"
        if not password2 or password != password2:
            ctx["password2_msg"] = "Hasła muszą być takie same"

        if name and surname and email and password and password2:
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
        is_active = True if request.POST.get('is_active') else False
        is_staff = True if request.POST.get('is_staff') else False

        # validation
        ctx = {}
        if not name:
            ctx["name_msg"] = "Podaj imię"
        if not surname:
            ctx["surname_msg"] = "Podaj nazwisko"
        if not email:
            ctx["email_msg"] = "Podaj email"

        if name and surname and email:
            user.first_name = name
            user.last_name = surname
            user.username = user.email = email
            user.is_active = is_active
            user.is_staff = is_staff
            user.save()
            return redirect('user-list')

        return render(request, 'user_update_form.html', ctx)


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
        ctx = {}
        if not name:
            ctx["name_msg"] = "Podaj imię"
        if not surname:
            ctx["surname_msg"] = "Podaj nazwisko"
        if not email:
            ctx["email_msg"] = "Podaj email"
        if not password:
            ctx["password_msg"] = "Podaj hasło aby zapisać zmiany"
        elif not check_password(password, user.password):
            ctx["password_msg"] = "Podane hasło jest nieprawidłowe"

        if name and surname and email and not ctx.get("password_msg"):
            user.first_name = name
            user.last_name = surname
            user.email = user.username = email
            user.save()
            return redirect('user-settings')

        return render(request, 'user_settings.html', ctx)


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
        ctx = {}
        if not old_password:
            ctx["old_password_msg"] = "Podaj swoje obecne hasło"
        elif not check_password(old_password, user.password):
            ctx["old_password_msg"] = "Podane hasło jest nieprawidłowe"
        if not new_password:
            ctx["new_password_msg"] = "Podaj nowe hasło"
        if not new_password2:
            ctx["new_password2_msg"] = "Powtórz nowe hasło"
        elif new_password != new_password2:
            ctx["new_password2_msg"] = "Hasła muszą być takie same"

        if not ctx.get("old_password_msg") and not ctx.get("new_password_msg") and not ctx.get("new_password2_msg"):
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
        donations = Donation.objects.filter(user=user).order_by("is_taken", "-pick_up_date")

        paginator = Paginator(donations, 20)
        # current page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        ctx = {
            'page_obj': page_obj,
        }
        return render(request, 'user_profile.html', ctx)


class UserDeleteView(StaffRequiredMixin, DeleteView):
    """
    Display confirmation and handle delete user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user-list')


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
