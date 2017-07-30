from django.shortcuts import render

# Create your views here.

# coding:utf-8
import json
import os
import time

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ueditor_index(request):
    """
    ueditor接入地址
    :param request:
    :return:
    """
    action = request.GET.get('action', '')
    if action == 'config':
        response_dict = settings.UEDITER_SETTING
        response_json = json.dumps(response_dict, ensure_ascii=False)
        return HttpResponse(response_json, content_type="application/javascript")
    elif action == 'uploadfile':
        return HttpResponse(ueditor_FileUp(request))
    elif action == 'uploadimage':
        return HttpResponse(ueditor_ImgUp(request))
    else:
        return HttpResponseBadRequest()

def format_file_name(name):
    '''
    去掉名称中的url关键字
    '''
    URL_KEY_WORDS = ['#', '?', '/', '&', '.', '%']
    for key in URL_KEY_WORDS:
        name_list = name.split(key)
        name = ''.join(name_list)
    return name

def my_upload_file(file_obj, file_type='pic'):
    """
    上传文件
    :param file_obj:
    :param file_type:
    :return:
    """
    if file_obj:
        filename = file_obj.name
        # filename = file_obj.name.decode('utf-8', 'ignore')
        filename_list = filename.split('.')
        file_postfix = filename_list[-1]  # 后缀
        # if file_postfix in ['txt', 'sql']:
        filename_list_clean = filename_list[:-1]
        file_name = ''.join(filename_list_clean) + str(int(time.time() * 1000))
        file_name = format_file_name(file_name)
        # else:
        #     file_name = str(uuid.uuid1())
        sub_folder = time.strftime("%Y%m")
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload', sub_folder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        absolute_path = os.path.join(upload_folder, file_name) + '.%s' % file_postfix
        if file_postfix.lower() in (
        "sql", "jpg", "jpeg", "bmp", "gif", "png", "xls", "xlsx", "rar", "doc", "docx", "zip", "pdf", "txt", "swf",
        "wmv"):
            destination = open(absolute_path, 'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()

            # if file_type == 'pic':  #暂不剪切图片
            #     if file_postfix.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
            #         im = Image.open(absolute_path)
            #         im.thumbnail((720, 720))
            #         im.save(absolute_path)

            real_url = os.path.join('/media/', 'upload', sub_folder, file_name) + '.%s' % file_postfix
            response_dict = {'original': filename, 'url': real_url, 'title': 'source_file_tile', 'state': 'SUCCESS',
                             'msg': ''}
        else:
            response_dict = {'original': filename, 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                             'msg': 'invalid file format'}
    else:
        response_dict = {'original': '', 'url': '', 'title': 'source_file_tile', 'state': 'FAIL',
                         'msg': 'invalid file obj'}
    return json.dumps(response_dict)


@csrf_exempt
def ueditor_ImgUp(request):
    """
    上传图片
    :param request:
    :return:
    """
    fileObj = request.FILES.get('upfile', None)
    response = HttpResponse()
    my_response = my_upload_file(fileObj, 'pic')
    response.write(my_response)
    return response


@csrf_exempt
def ueditor_FileUp(request):
    """ 上传文件 """
    fileObj = request.FILES.get('upfile', None)
    response = HttpResponse()
    my_response = my_upload_file(fileObj, 'file')
    response.write(my_response)
    return response
