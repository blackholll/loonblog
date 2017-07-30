import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image, ImageDraw, ImageFont
from django.http.response import HttpResponse
import io, string, os, random

from django.views.decorators.http import require_http_methods

from services.comment.comment_service import CommentService
from services.common.ip_service import IpService
from services.common.msg_service import MsgService

BASE_DIR = settings.BASE_DIR

logger = logging.getLogger('default')

# Create your views here.

def index(request):
    pass

def captcha(request):
    """
    验证码。 后续会加入一些干扰，如弯曲、背景干扰等
    :param request:
    :return:
    """
    image = Image.new('RGB', (91, 31), color=(255, 255, 255))  # model, size, background color
    font_file = os.path.join(BASE_DIR, 'static/fonts/Arial.ttf')  # choose a font file
    font = ImageFont.truetype(font_file, 30)  # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))  # The random string
    draw.text((7, 0), rand_str, fill=(0, 0, 0), font=font)  # position, content, color, font
    del draw
    request.session['captcha'] = rand_str.lower()  # store the content in Django's session store
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "JPEG")
    return response


@require_http_methods(['POST'])
def comment(request, blog_id):
    """
    评论
    :param blog_id:
    :param request:
    :return:
    """
    post_data = request.POST
    captcha = post_data.get('captcha', '')
    if captcha != request.session["captcha"]:
        return JsonResponse({'code': 500, 'msg': '验证码错误'})
    else:
        ip, msg = IpService().get_client_ip(request)
        # black_list = ['46.161.9.29', ]  # 改成通过nginx限制
        # if ip in black_list:
        #     logger.info('黑名单尝试评论失败：%s' % ip)
        #     return JsonResponse({'code': 500, 'msg': '你已经被拉黑，请勿刷评论, you are in blacklist'})
        name = post_data.get('name', '')
        email = post_data.get('email', '')
        comment_content = post_data.get('comment_content', '')
        creator = request.user.username   # 可为空
        username = request.user.username
        is_recomment = post_data.get('is_recomment', '')
        obj_type_id = 2 if is_recomment else 1
        obj_id = is_recomment if is_recomment else blog_id

        if is_recomment:  # 对留言的回复，通知留言者
            recomment_obj, msg = CommentService.get_comment_by_id(is_recomment)
            recomment_email = recomment_obj[0].email
        else:
            admin_email = settings.ADMIN_EMAIL  #管理员邮箱
            recomment_email = admin_email

        params = dict(name=name, email=email, content=comment_content, source_ip=ip, obj_type_id=obj_type_id,
                      obj_id=obj_id, creator=creator, username=username, blog_id=blog_id,
                      recomment_email=recomment_email)

        flag, msg = CommentService().add_comment(params)
        if flag:
            return JsonResponse({'code': 200, 'msg': '评论成功'})
        else:
            return JsonResponse({'code': 500, 'msg': '发生错误'+msg})





