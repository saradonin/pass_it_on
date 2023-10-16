from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from pass_it_on_app.models import Institution, Donation, User


class IndexView(View):
    """
    View for rendering the index page.
    """

    def get(self, request):
        bags_given_count = 0
        institutions_supported = []
        for donation in Donation.objects.all():
            bags_given_count += donation.quantity
            # TODO possible refactor
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


class UserLogoutView(View):
    """
    View for user logout.
    """

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


class DonationAddView(View):
    """
    View for rendering the donation form.
    """

    def get(self, request):
        return render(request, 'form.html')
