import datetime
from django.db import transaction
from django.db.models import Q
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from apps.blog.models import Blog, BlogTag
from services.base_service import BaseService
from services.blog.blog_tag_service import BlogTagService
from services.blog.category_service import CategoryService
from services.blog.topic_service import TopicService
from services.comment.comment_service import CommentService
from services.common.auto_log_service import auto_log

class BlogService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_blog_list_by_page(page, size=5, category_id=None):
        """
        分页获取文章列表obj
        :return:
        """
        if category_id:
            base_query_dict = dict(is_deleted=False, category_id=category_id)
        else:
            base_query_dict = dict(is_deleted=False)

        total_count = Blog.objects.filter(**base_query_dict).count()

        # if category_id:
        #     total_count = Blog.objects.filter(is_deleted=False, category_id=category_id).count()
        # else:
        #     total_count = Blog.objects.filter(is_deleted=False).count()

        if total_count/size == 0:
            total_page = 1
        elif total_count/float(size) > total_count/size:
            total_page = total_count/size +1
        else:
            total_page = total_count/size



        if page:
            if page <= total_page:
                start = (page-1)*size
                end = page*size
                query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')[start:end]
                # if category_id:
                #     query_result = Blog.objects.filter(is_deleted=False, category_id=category_id).order_by('-gmt_created')[start:end]
                # else:
                #     query_result = Blog.objects.filter(is_deleted=False).order_by('-gmt_created')[start:end]
            else:
                # query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')[-size:-1]  #不支持负索引

                if total_count-size >0 :
                    query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')[
                                   (total_count-size):total_count]
                else:
                    query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')

                # query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')[abs(size-total_count):total_count]
                # if category_id:
                #     query_result = Blog.objects.filter(is_deleted=False, category_id=category_id).order_by('-gmt_created')[-size:-1]
                # else:
                #     query_result = Blog.objects.filter(is_deleted=False).order_by('-gmt_created')[-size:-1]
        else:
            query_result = Blog.objects.filter(**base_query_dict).order_by('-gmt_created')[:size]
            # if category_id:
            #     query_result = Blog.objects.filter(is_deleted=False, category_id=category_id).order_by('-gmt_created')[:size]
            # else:
            #     query_result = Blog.objects.filter(is_deleted=False).order_by('-gmt_created')[:size]
        return query_result, [total_count,total_page]

    @staticmethod
    @auto_log
    def get_json_list(query_contains, query_control):
        """
        获取文章列表
        :param query_contains: 模糊查询条件
        :param query_control: 控制条件
        :return:
        """
        length = int(query_control['length'])  # 每页显示条数
        start = int(query_control['start'])  # 第几条
        end = start + length - 1
        all_result_count = Blog.objects.all().count()
        if query_contains:
            # 尝试使用rawsql，总是有问题， 暂时放弃
            # sql_str = 'select *, b.name as category_name , c.name as topic_name from blog_blog a join blog_category b on a.`category_id`=b.id join `blog_topic` c on a.`topic_id`=c.id and (a.title like "%{}%" or a.content like "%{}%") limit {},{}'.format(query_contains,query_contains,start,end1)
            # query_result = Blog.objects.raw(sql_str)
            query_result = Blog.objects.filter(Q(title__contains=query_contains) | Q(content__contains=query_contains)
                                               )[start:end]
            result_dict_list = []
            for query_result0 in query_result:
                result_dict = {}
                # result_dict['title'] = query_result0.title
                result_dict['title'] = '<a href = "/blog/edit/{}">{}</a>'.format(query_result0.id, query_result0.title)
                category_query, msg = CategoryService.get_category_by_id(query_result0.category_id)
                if category_query:
                    result_dict['category'] = category_query[0].name

                topic_query, msg = TopicService.get_topic_by_id(query_result0.topic_id)
                if topic_query:
                    result_dict['topic'] = topic_query[0].name
                tags, msg = BlogTagService.get_tags_by_blog_id(query_result0.id)
                if tags:
                    result_dict['tag'] = tags
                else:
                    result_dict['tag'] = ''

                result_dict['comment_times'], msg = CommentService.get_comment_count_by_blog_id(query_result0.id)
                result_dict['is_deleted'] = '是' if query_result0.is_deleted else '否'
                result_dict['gmt_created'] = str(query_result0.gmt_created)[0:19]
                result_dict_list.append(result_dict)
            query_count = query_result.count()
            filter_count = query_count

        else:
            query_result = Blog.objects.raw('select *, b.name as category_name from blog_blog a '
                                            'join blog_category b on a.`category_id`=b.id limit %d,%d' % (start, length))
            result_dict_list = []
            for query_result0 in query_result:
                result_dict = {}
                result_dict['title'] = query_result0.title
                result_dict['title'] = '<a href = "/blog/edit/{}">{}</a>'.format(query_result0.id, query_result0.title)
                # result_dict['content'] = query_result0.content
                result_dict['category'] = query_result0.category_name
                tags, msg = BlogTagService.get_tags_by_blog_id(query_result0.id)
                if tags:
                    result_dict['tag'] = tags
                else:
                    result_dict['tag'] = ''

                result_dict['comment_times'], msg = CommentService.get_comment_count_by_blog_id(query_result0.id)

                result_dict['is_deleted'] = '是' if query_result0.is_deleted else '否'
                result_dict['gmt_created'] = str(query_result0.gmt_created)[0:19]
                result_dict_list.append(result_dict)
            query_count = len(list(query_result))
            filter_count = all_result_count
        return result_dict_list, [query_count, all_result_count, filter_count]

    @staticmethod
    @auto_log
    # @transaction.commit_manually  #暂时不使用事务，新增错误影响不大
    def add_blog(kwargs):
        """
        新增文章
        :param kwargs:
        :return:
        """
        blog_obj = Blog(topic_id=kwargs['topic_id'], content=kwargs['content'], title=kwargs['title'],
                                category_id=kwargs['category_id'], creator=kwargs['creator'])
        blog_obj.save()
        blog_id = blog_obj.id
        queryset_list = []
        tag_id_list = kwargs['tag_id_list']
        for tag_id in tag_id_list:
            queryset_list.append(BlogTag(blog_id=blog_id, tag_id=tag_id, creator=kwargs['creator']))
        BlogTag.objects.bulk_create(queryset_list)
        return True, ''

    @staticmethod
    @auto_log
    # @transaction.commit_manually  #暂时不使用事务，新增错误影响不大
    def edit_blog(kwargs):
        """
        编辑文章
        :param kwargs:
        :return:
        """
        blog_id = kwargs['blog_id']
        creator = kwargs['creator']
        blog_obj = Blog.objects.filter(id=blog_id)
        tag_id_list = kwargs['tag_id_list']
        del kwargs['blog_id']
        del kwargs['tag_id_list']
        del kwargs['creator']
        now_time = datetime.datetime.now()
        kwargs['gmt_modified'] = now_time
        blog_obj.update(**kwargs)
        BlogTag.objects.filter(blog_id=blog_id, is_deleted=False).delete()
        queryset_list = []
        for tag_id in tag_id_list:
            queryset_list.append(BlogTag(blog_id=blog_id, tag_id=tag_id, creator=creator))
        BlogTag.objects.bulk_create(queryset_list)
        return True, ''

    @staticmethod
    @auto_log
    def get_blog_by_id(id, exclude_deleted=False):
        """
        获取blog信息
        :param id:
        :param exclude_deleted:排除已经删除的
        :return:
        """
        if exclude_deleted:
            return Blog.objects.filter(id=id, is_deleted=False), ''
        else:
            return Blog.objects.filter(id=id), ''

    @staticmethod
    @auto_log
    def update_view_count(blog_id):
        """
        更新文章访问次数,计算准确访问次数的时候需要把这个也加上
        :param blog_id:
        :return:
        """
        key_flag = 'blog_view_count_%d' % blog_id
        view_count = cache.get(key_flag)
        if view_count != None:
            cache.incr(key_flag)
            if not (view_count % 10):   # 当发现访问次数是10的倍数， 就更新数据库中文章访问次数
                Blog.objects.filter(id=blog_id).update(view_count=view_count)

        else:  # 缓存中没有访问次数记录，则从数据库中获取
            view_count = Blog.objects.get(id=blog_id).view_count
            cache.set(key_flag, view_count+1, None)  # 永不过期

    @staticmethod
    @auto_log
    def get_new_blog(num=5):
        """
        最近更新的5条博客,包括编辑过和新增的
        :param num:
        :return:
        """
        return Blog.objects.filter(is_deleted=False).order_by('-gmt_modified')[:num], ''

    @staticmethod
    @auto_log
    def get_hot_blog(num=5):
        """
        最热门5条博客，点击次数排行， 直接通过数据库中字段判断，不考虑缓存中的最新访问次数
        :param num:
        :return:
        """
        return Blog.objects.filter(is_deleted=False).order_by('-view_count', '-gmt_modified')[:num], ''