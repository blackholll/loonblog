from apps.blog.models import BlogTag
from services.base_service import BaseService
from services.blog.tag_service import TagService
from services.common.auto_log_service import auto_log


class BlogTagService(BaseService):
    """
    标签service
    """

    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_tags_by_blog_id(blog_id):
        """
        获取文章的标签信息
        :param blog_id:
        :return:
        """

        tag_list = []
        tag_query = BlogTag.objects.filter(blog_id=blog_id)
        for tag_query0 in tag_query:
            tag_id = tag_query0.tag_id
            taginfo, msg = TagService.get_tag_by_id(tag_id)
            tag_name = taginfo[0].name
            tag_list.append(tag_name)
        return ','.join(tag_list), ''

    @staticmethod
    @auto_log
    def get_tag_list_by_blog_id(blog_id):
        """
        获取文章标签列表
        :param blog_id:
        :return:
        """
        tag_list = []
        tag_query = BlogTag.objects.filter(blog_id=blog_id)
        for tag_query0 in tag_query:
            tag_id = tag_query0.tag_id
            tag_info, msg = TagService.get_tag_by_id(tag_id)
            tag_id = tag_info[0].id
            tag_list.append(tag_id)
        return tag_list, ''

    @staticmethod
    @auto_log
    def get_tag_obj_list_by_blog_id(blog_id):
        """
        获取文章标签对象列表
        :param blog_id:
        :return:
        """
        tag_query = BlogTag.objects.raw('select *, b.name as tag_name from blog_blogtag a join blog_tag b on '
                                        'a.`tag_id`=b.`id` where a.is_deleted=0 and a.blog_id= {}'.format(blog_id))

        return tag_query, ''

