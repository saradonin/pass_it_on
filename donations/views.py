from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from donations.models import Institution, Donation, Category


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
        non_gov_organizations = Institution.objects.filter(
            type="2").order_by("name")
        local_collections = Institution.objects.filter(
            type="3").order_by("name")

        ctx = {
            "institutions_supported": len(institutions_supported),
            "bags_given": bags_given_count,
            "foundations": foundations,
            "non_gov_organizations": non_gov_organizations,
            "local_collections": local_collections,
        }
        return render(request, 'index.html', ctx)


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
        categories = request.POST.getlist('categories')
        quantity = request.POST.get('bags')
        institution_name = request.POST.get('organization')
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
