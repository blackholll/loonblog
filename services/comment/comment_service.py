from services.base_service import BaseService
from services.common.auto_log_service import auto_log
from apps.comment.models import Comment
from services.common.msg_service import MsgService
import logging
logger = logging.getLogger('default')


class CommentService(BaseService):
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def get_comment_count_by_blog_id(obj_id, obj_type_id=1):
        """
        获取评论个数
        :param obj_id: 评论对象
        :param obj_type_id: 评论对象类别  #1.博客 2.
        :return:
        """
        return Comment.objects.filter(obj_id=obj_id, obj_type_id=obj_type_id).count(), ''

    @staticmethod
    @auto_log
    def add_comment(kwargs):
        """
        新增评论
        :param kwargs:
        :return:
        """
        # 不允许包含http
        if 'http://' in kwargs['content']:
            source_ip = kwargs['source_ip']
            logger.info('*'*30)
            logger.info('评论中包含http,来源:%s' % source_ip)
            logger.info(kwargs['content'])
            logger.info('*' * 30)
            return False, '非法内容,禁止评论。如有疑问请直接联系博主（页面顶部"关于"中有联系方式）'

        blog_id = kwargs['blog_id']
        recomment_email = kwargs['recomment_email']
        kwargs.pop('blog_id')
        kwargs.pop('recomment_email')
        comment_obj = Comment(**kwargs)
        comment_obj.save()

        if kwargs['creator'] == 'admin' or kwargs['obj_type_id'] != 2:  # 管理员留言或者给管理员留言的情况才发送邮件通知
            # MsgService().send_email_by_process('来自loonapp的留言提醒',
            #                                    '你有一条新的留言，请登录查看: http://loonapp.com/blog/{}/'.format(blog_id),
            #                                    [kwargs['email']])

            MsgService().send_multi_email_by_process('来自loonapp的留言提醒',
                                               '<p>你有一条新的留言，<a href="http://loonapp.com/blog/{}/">请点击查看</a>'.format(blog_id),
                                               [recomment_email])

        return True, comment_obj

    @staticmethod
    @auto_log
    def get_comment_by_blog_id(obj_id, obj_type_id=1):
        """
        获取评论
        :param obj_id:
        :param obj_type_id:
        :return:
        """
        return Comment.objects.filter(obj_id=obj_id, obj_type_id=obj_type_id, is_deleted=False), ''

    @staticmethod
    @auto_log
    def get_comment_by_id(comment_id):
        """
        获取评论
        :param comment_id:
        :return:
        """
        return Comment.objects.filter(id=comment_id, is_deleted=False), ''



