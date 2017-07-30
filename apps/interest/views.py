from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from services.about.about_service import AboutService

@cache_page(300)
def index(request):
    return render(request, 'interest/index.html')
