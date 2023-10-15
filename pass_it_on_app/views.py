from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexView(View):
    """
    View for rendering the index page.
    """

    def get(self, request):
        return render(request, 'index.html')
