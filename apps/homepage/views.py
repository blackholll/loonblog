from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from services.blog.blog_service import BlogService
from services.blog.category_service import CategoryService

# @cache_page(300)
def index(request):
    """
    首页-
    :param request:
    :return:
    """
    top_categorys, msg = CategoryService.get_top_category()
    new_blogs, msg1 = BlogService.get_new_blog()
    hot_blogs, msg2 = BlogService.get_hot_blog()
    params = dict(top_categorys=top_categorys, new_blogs=new_blogs, hot_blogs=hot_blogs)
    return render(request, 'index.html', params)
