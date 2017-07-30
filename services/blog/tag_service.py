from apps.blog.models import Tag
from services.base_service import BaseService
from services.common.auto_log_service import auto_log


class TagService(BaseService):
    """
    标签service
    """

    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_tag_list():
        """
        获取标签列表
        :return:
        """
        return Tag.objects.filter(is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_tag_by_id(id):
        """
        获取标签信息
        :param id:
        :return:
        """
        return Tag.objects.filter(id=id), ''
