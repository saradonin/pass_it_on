from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

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

        foundations = Institution.objects.filter(type=1).order_by("name")
        non_gov_organizations = Institution.objects.filter(type=2).order_by("name")
        local_collections = Institution.objects.filter(type=3).order_by("name")

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


class UserAddView(View):
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
            ctx["password_msg"] = "Hasło musi zaiwerać co najmniej 8 znaków"
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
    View for rendering the donation form.
    """
    login_url = "/login/"

    def get(self, request):
        return render(request, 'form-confirmation.html')
