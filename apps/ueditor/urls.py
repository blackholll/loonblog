from django.conf.urls import url
from apps.ueditor.views import ueditor_index,ueditor_ImgUp, ueditor_FileUp


urlpatterns = [
    url(r'^$', ueditor_index),
    url(r'^ueditor_imgup/$', ueditor_ImgUp),
    url(r'^ueditor_fileup/$', ueditor_FileUp),
]
