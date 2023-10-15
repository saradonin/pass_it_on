from django.shortcuts import render
from django.views import View

from pass_it_on_app.models import Institution, Donation


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
