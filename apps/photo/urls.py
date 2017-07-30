from django.conf.urls import url
from apps.photo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

]