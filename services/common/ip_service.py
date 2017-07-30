from services.base_service import BaseService
from services.common.auto_log_service import auto_log


class IpService(BaseService):
    """
    ip地址服务
    """
    def __int__(self):
        pass

    @staticmethod
    @auto_log
    def get_client_ip(request):
        """
        获取客户端ip地址
        :param request:
        :return:
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip, ''
