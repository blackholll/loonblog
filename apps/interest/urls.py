from django.conf.urls import url
from apps.interest import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

]