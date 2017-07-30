from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from services.about.about_service import AboutService

# @cache_page(300)
def index(request):
    about_service_obj = AboutService()
    about_mes, msg = about_service_obj.get_about_me_list()
    about_loonapps, msg2 = about_service_obj.get_about_loonapp_list()
    about_copyrights, msg2 = about_service_obj.get_about_copyright_list()
    return render(request, 'about/about.html', dict(about_mes=about_mes, about_loonapps=about_loonapps,
                                                    about_copyrights=about_copyrights))
