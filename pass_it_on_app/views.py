from django.shortcuts import render
from django.views import View


class IndexView(View):
    """
    View for rendering the index page.
    """

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    """
    View for rendering the login page.
    """

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    """
    View for rendering the register page.
    """

    def get(self, request):
        return render(request, 'register.html')


class DonationAddView(View):
    """
    View for rendering the donation form.
    """

    def get(self, request):
        return render(request, 'form.html')
