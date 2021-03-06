import json
import os

from django.http import HttpResponse
from login.models import MyUser, Test


def get_test(request):
    users = []
    list = MyUser.objects.all()
    if request.method == 'GET':
        for var in list:
            user = {}
            user['id'] = var.isOnline
            user['name'] = var.username
            user['sex'] = var.password
            users.append(user)
    return HttpResponse(json.dumps(users))  # 返回user数据给安卓端


def post_test(request):
    if request.method == 'POST':
        print(request.POST)
        req = request.POST.get('v1')  # 获取post请求中的v1所对应的值
        print('post请求')
        print(req)
        return HttpResponse(req)  # 返回v1所对应的值 -- 只是用来测试代码，实际逻辑按自己要求来
    else:
        return HttpResponse("none")


def upload_file(request):
    if request.method == 'POST':
        print('post: ')
        print(request.POST)
        print(request.FILES)
    return HttpResponse('success')
    # print('post: ')
    # temp_file = request.FILES
    # if not temp_file:
    #     print("文件传输失败")
    #     return HttpResponse('upload failed!')
    # else:
    #     print("文件传输成功")
    #     print('temp: ' + temp_file)
    #     return HttpResponse('upload failed!')
    #     # TODO: 获取图片并存储在./uploads目录下 -- 实际逻辑按自己要求来
    #     destination = open(os.path.join("./uploads", temp_file.get('file').name), 'wb+')
    #     for chunk in temp_file.get('file').chunks():
    #         destination.write(chunk)
    #     destination.close()
    # return HttpResponse('upload success!')


def test_file(request):
    if request.method == 'POST':
        print(request.FILES)

        kwargs = {
            'name': 'drdese',
            'headImg': request.FILES.get('file'),
        }
        temp = Test.objects.create(**kwargs)
        temp.save()
    return HttpResponse('success')
