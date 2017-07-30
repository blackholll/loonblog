from django.conf.urls import url
from apps.comment import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^captcha/$', views.captcha, name='captcha'),
    url(r'^(\d+)/$', views.comment, name='comment'),

]