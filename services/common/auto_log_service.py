import logging
import traceback

logger = logging.getLogger('default')


def auto_log(func):
    """
    自动记录日志的装饰器：
    :param func:
    :return:
    """
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc())
            return False, e.__str__()

    return _deco


def auto_class_log(some_class):
    """
    类装饰器
    :param some_class:
    :return:
    """
    pass
    #  貌似没法通过对类加装饰器实现类里面所有方法都加入装饰器处理， 以后有时间再研究下