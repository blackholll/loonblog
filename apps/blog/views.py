import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models.query import QuerySet

from services.blog.blog_service import BlogService
from services.blog.blog_tag_service import BlogTagService
from services.blog.category_service import CategoryService
from services.blog.tag_service import TagService
from services.blog.topic_service import TopicService
# Create your views here.
from services.comment.comment_service import CommentService


@cache_page(300)
def index(request):
    """
    文章首页
    :param request:
    :return:
    """
    page = request.GET.get('page', 0)
    page = int(page) if page else ''
    cat = request.GET.get('cat', 0)
    cat = int(cat) if cat else ''


    if cat:
        blogs, msg = BlogService.get_blog_list_by_page(page, category_id=cat)
    else:
        blogs, msg = BlogService.get_blog_list_by_page(page)
    if blogs or isinstance(blogs, QuerySet):
        total_count = msg[0]
        total_page = int(msg[1])
    else:
        return HttpResponseServerError
    blog_list = []
    for blog in blogs:
        blog_dict = {}
        blog_dict['title'] = blog.title
        blog_dict['id'] = blog.id
        blog_dict['gmt_created'] = blog.gmt_created
        blog_dict['content'] = blog.content
        blog_dict['category'] = blog.category_id
        category_query, msg = CategoryService.get_category_by_id(blog.category_id)
        if category_query:
            blog_dict['category'] = category_query[0].name
        else:
            blog_dict['category'] = ''

        topic_query, msg = TopicService.get_topic_by_id(blog.topic_id)
        if topic_query:
            blog_dict['topic'] = topic_query[0].name
        else:
            blog_dict['topic'] = ''

        blog_tag_query, msg = BlogTagService.get_tag_obj_list_by_blog_id(blog.id)
        blog_dict['blog_tag_query'] = blog_tag_query
        blog_list.append(blog_dict)
    if not page:
        page = 1

    if page < total_page:
        has_next = True
    else:
        has_next = False
    if (page >= 2) and (total_page) >2:
        has_pre = True
    else:
        has_pre = False

    category_list_query, msg4 = CategoryService.get_category_list()
    tag_list_query, msg4 = TagService.get_tag_list()
    topic_list_query, msg4 = TopicService.get_topic_list()

    params = dict(blogs=blog_list, total_count=total_count, total_page=total_page, page=page,has_next=has_next,
                  has_pre=has_pre, category_list_query=category_list_query, tag_list_query=tag_list_query,
                  topic_list_query=topic_list_query, cat=cat)

    return render(request, 'blog/blog_index.html', params)


@login_required
@csrf_exempt  # 暂时通过exempt来支持ajax。后续有时间改下
def get_json_list(request):
    """
    json格式blog列表
    :param request:
    :return:
    """
    request_data = request.POST
    draw = request_data.get('draw', '')
    start = request_data.get('start', '')
    search_value = request_data.get('search[value]', '')
    length = request_data.get('length', '')

    query_contains = search_value

    query_control = dict(start=start, length=length)

    data, msg = BlogService.get_json_list(query_contains, query_control)

    return HttpResponse(json.dumps({"draw": draw, "recordsTotal": msg[1], "recordsFiltered": msg[2], "data": data}),
                            content_type='application/json')


# @cache_page(300) # 因为留言后刷新页面，用缓存的话 会导致页面不更新，暂时去掉
def blog_view(request, blog_id):
    """
    文章查看
    :param request:
    :param blog_id:
    :return:
    """
    BlogService.update_view_count(int(blog_id))
    blog_query, msg = BlogService.get_blog_by_id(blog_id, True)
    blog_dict = {}
    if blog_query:
        blog_dict['id'] = blog_query[0].id
        blog_dict['title'] = blog_query[0].title
        blog_dict['gmt_created'] = blog_query[0].gmt_created
        blog_dict['content'] = blog_query[0].content
        blog_dict['category_id'] = blog_query[0].category_id
        category_query, msg = CategoryService.get_category_by_id(blog_query[0].category_id)
        if category_query:
            blog_dict['category'] = category_query[0].name
        else:
            blog_dict['category'] = ''
        topic_query, msg = TopicService.get_topic_by_id(blog_query[0].topic_id)
        if topic_query:
            blog_dict['topic'] = topic_query[0].name
        else:
            blog_dict['topic'] = ''

        blog_tag_query, msg = BlogTagService.get_tag_obj_list_by_blog_id(blog_query[0].id)
        blog_dict['blog_tag_query'] = blog_tag_query
    else:
        return render(request, '404.html')
    category_list_query, msg4 = CategoryService.get_category_list()
    tag_list_query, msg4 = TagService.get_tag_list()
    topic_list_query, msg4 = TopicService.get_topic_list()

    comment_list_query, msg5 = CommentService().get_comment_by_blog_id(obj_id=blog_id)

    params = dict(blog=blog_dict, category_list_query=category_list_query, tag_list_query=tag_list_query,
                  topic_list_query=topic_list_query, comment_list_query=comment_list_query)


    return render(request, 'blog/blog_view.html', params)


@login_required
def blog_list(request):
    """
    博客管理列表
    :param request:
    :param id:
    :return:
    """
    return render(request, 'blog/blog_list.html')


@login_required
@require_http_methods(['GET', 'POST'])
def blog_add(request):
    """
    新增文章
    :param request:
    :return:
    """

    request_method = request.method
    if request_method == 'GET':
        category_list, msg1 = CategoryService.get_category_list()
        tag_list, msg2 = TagService.get_tag_list()
        topic_list, msg3 = TopicService.get_topic_list()
        params = dict(category_list=category_list, tag_list=tag_list, topic_list=topic_list, page_title='新增文章')
        params['post_url'] = '/blog/add/'
        return render(request, 'blog/blog_edit.html', params)
    elif request_method == 'POST':
        post_data = request.POST
        title = post_data.get('title', '')
        topic_id = post_data.get('topic', '')
        category_id = post_data.get('category', '')
        content = post_data.get('content', '')
        tag_id_list = post_data.getlist('tag', [])
        creator = request.user.username
        params = dict(title=title, topic_id=topic_id, category_id=category_id, content=content, tag_id_list=tag_id_list,
        creator=creator)
        flag, msg = BlogService.add_blog(params)
        if flag:
            return HttpResponseRedirect('/blog/list/')
        else:
            return HttpResponse('新增失败:{}'.format(msg))


@login_required
@require_http_methods(['GET', 'POST'])
def blog_edit(request, blog_id):
    """
    编辑文章
    :param request:
    :param blog_id:
    :return:
    """
    request_method =request.method
    category_list, msg1 = CategoryService.get_category_list()
    tag_list, msg2 = TagService.get_tag_list()
    topic_list, msg3 = TopicService.get_topic_list()
    params = dict(category_list=category_list, tag_list=tag_list, topic_list=topic_list, page_title='编辑文章')

    if request_method == 'GET':
        query_result, msg = BlogService.get_blog_by_id(blog_id)

        tag_query_list, msg1 = BlogTagService.get_tag_list_by_blog_id(blog_id)

        if query_result:
            params['query_result0'] = query_result[0]
            params['tag_query_list'] = tag_query_list
            params['post_url'] = '/blog/edit/{}/'.format(blog_id)
            return render(request, 'blog/blog_edit.html', params)
        else:
            return HttpResponse('Error:文章不存在')

    else:
        post_data = request.POST
        title = post_data.get('title', '')
        topic_id = post_data.get('topic', '')
        category_id = post_data.get('category', '')
        content = post_data.get('content', '')
        tag_id_list = post_data.getlist('tag', [])
        creator = request.user.username
        params = dict(title=title, topic_id=topic_id, category_id=category_id, content=content, tag_id_list=tag_id_list,
                      blog_id=blog_id, creator=creator)
        flag, msg = BlogService.edit_blog(params)
        if flag:
            return HttpResponseRedirect('/blog/list/')
        else:
            return HttpResponse('编辑失败:{}'.format(msg))
