from django.conf.urls import url
from apps.about import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

]