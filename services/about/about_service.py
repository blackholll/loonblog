from apps.about.models import AboutMe, AboutLoonapp, AboutCopyright
from services.base_service import BaseService
from services.common.auto_log_service import auto_log


class AboutService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_about_me_list():
        """关于我"""
        return AboutMe.objects.filter(is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_about_loonapp_list():
        """关于lonnapp"""
        return AboutLoonapp.objects.filter(is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_about_copyright_list():
        """关于"""
        return AboutCopyright.objects.filter(is_deleted=False), ''
