from django.conf import settings


def now_env(request):
    """
    获取当前环境
    :param request:
    :return:
    """
    env = settings.ENV
    return {'now_env': env}
