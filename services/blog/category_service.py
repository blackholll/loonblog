from apps.blog.models import Category
from services.base_service import BaseService
from services.common.auto_log_service import auto_log


class CategoryService(BaseService):
    """
    分类service
    """
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_category_list():
        """
        获取分类列表
        :return:
        """
        return Category.objects.filter(is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_category_by_id(id):
        """
        获取分类信息
        :param id:
        :return:
        """
        return Category.objects.filter(id=id), ''

    @staticmethod
    @auto_log
    def get_top_category(top=5):
        """
        获取具有数量最多blog的前top分类
        :return:
        """
        result = Category.objects.raw("select b.id, b.name, count(*) as count from blog_blog a join blog_category b on a.`category_id`=b.id group by(category_id)")
        return result[:top], ''
