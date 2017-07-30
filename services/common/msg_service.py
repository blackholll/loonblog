import os
import multiprocessing
from multiprocessing import Process
from django.core.mail import send_mail,EmailMultiAlternatives
from services.base_service import BaseService
from services.common.auto_log_service import auto_log
import logging
logger = logging.getLogger('default')

class MsgService(BaseService):
    """
    消息服务
    """
    def __init__(self):
        pass

    @staticmethod
    @auto_log
    def send_email_by_process(subject, content, mail_to_list):
        """
        发送邮件
        :param subject:
        :param content:
        :param mail_to_list:收件人
        :return:
        """
        # logger.info('同步发送')
        # a = send_mail(subject, content, 'LOONAPP<loonapp@163.com>', mail_to_list)
        # logger.info(a)
        # logger.info('后台发送')
        logger.info('发送邮件:{}-{}-{}'.format(subject, content, mail_to_list))
        p = multiprocessing.Process(target=send_mail, args=(subject, content, 'LOONAPP<loonapp@163.com>', mail_to_list))
        p.start()
        return True, ''

    @staticmethod
    @auto_log
    def send_multi_email_by_process(subject, content, mail_to_list):
        logger.info('发送html邮件:{}-{}-{}'.format(subject, content, mail_to_list))
        msg = EmailMultiAlternatives(subject, content,from_email='LOONAPP<loonapp@163.com>',to=mail_to_list)
        msg.content_subtype = "html"
        p = multiprocessing.Process(target=msg.send, args=())
        p.start()


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
    MsgService().send_email_by_process('test', 'testt',['blackholll@163.com'])
    MsgService().send_multi_email_by_process('test', '<a href="http://www.baidu.com">百度</a>',['blackholll@163.com'])

