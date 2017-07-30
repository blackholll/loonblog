from django.conf.urls import url
from apps.blog import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)/$', views.blog_view, name='blog_view'),
    url(r'^list/$', views.blog_list, name='list'),
    url(r'^add/$', views.blog_add, name='add'),
    url(r'^get_json_list/$', views.get_json_list, name="get_json_list"),
    url(r'^edit/(\d+)/$', views.blog_edit, name="edit"),

]