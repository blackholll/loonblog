"""loonblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.homepage.views import index
from apps.blog import urls as blog_urls
from apps.ueditor import urls as ueditor_urls
from apps.comment import urls as comment_urls
from apps.about import urls as about_urls
from apps.photo import urls as photo_urls
from apps.interest import urls as interest_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^blog/', include(blog_urls, namespace="blog")),
    url(r'^ueditor/', include(ueditor_urls, namespace="ueditor")),
    url(r'^comment/', include(comment_urls, namespace="comment")),
    url(r'^about/', include(about_urls, namespace="about")),
    url(r'^photo/', include(photo_urls, namespace="photo")),
    url(r'^interest/', include(interest_urls, namespace="interest")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
