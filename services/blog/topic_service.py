from apps.blog.models import Topic
from services.base_service import BaseService
from services.common.auto_log_service import auto_log


class TopicService(BaseService):
    """
    专题service
    """

    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_topic_list():
        """
        获取主题列表
        :return:
        """
        return Topic.objects.filter(is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_topic_by_id(id):
        """
        获取主题信息
        :param id:
        :return:
        """
        return Topic.objects.filter(id=id),  ''
