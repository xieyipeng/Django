import json

from django.contrib import auth

from django.http import HttpResponse
from login.models import MyUser, Friend, Dynamic


# https://docs.djangoproject.com/en/2.1/topics/auth/default/
def register(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = MyUser.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse('success')
    except BaseException as e:
        return HttpResponse(e.__str__())


def user_login(request):
    try:
        if request.method == 'POST':
            print(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                data = {
                    'username': user.username,
                    'headImg': user.headImg.__str__().split('./uploads/')[1],
                    'date_joined': user.date_joined.__str__().split(' ')[0],
                    'last_login': user.last_login.__str__(),
                }
                return HttpResponse(json.dumps(data))
            else:
                return HttpResponse('password_error')
    except Exception as e:
        print('error: ' + e.__str__())
        return HttpResponse(e.__str__())


def user_logout(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # user = MyUser.objects.get(pk=username)
        # if user.is_active:
        #     user.is_active = False
        return HttpResponse('success')

    return HttpResponse('failed')


def check_is_friend(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            user = MyUser.objects.get(pk=request.POST.get('friend_name'))
        except Exception as e:
            print('error: ' + e.__str__())
            user = None
        if user:
            return HttpResponse('exist')
        else:
            return HttpResponse('in_exist')


def add_friend(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            friend_one = MyUser.objects.get(pk=request.POST.get('my_name'))
            friend_other = MyUser.objects.get(pk=request.POST.get('friend_name'))

            list = Friend.objects.all()
            for var in list:
                if var.friend_other.username == request.POST.get(
                        'friend_name') and var.friend_one.username == request.POST.get('my_name'):
                    print('已经添加')
                    return HttpResponse('have add')
            friend = Friend.objects.create(friend_one=friend_one, friend_other=friend_other)
            friend.save()
            return HttpResponse('success')
        except Exception as e:
            print('error: ' + e.__str__())
            return HttpResponse('error')


def get_all_friend(request):
    friends = []
    list = Friend.objects.all()
    if request.method == 'POST':
        for var in list:
            print('name: '+request.POST.get('my_name'))
            print(var.friend_one.username)
            if var.friend_one.username == request.POST.get('my_name'):
                friend = {}
                friend['name'] = var.friend_other.username
                friend['headImg'] = var.friend_other.headImg.__str__().split('./uploads/')[1]
                friend['isOnline'] = var.friend_other.isOnline

                friends.append(friend)
    import json
    print(json.dumps(friends))
    return HttpResponse(json.dumps(friends))  # 返回user数据给安卓端


def get_all_friend_message(request):
    friends = []
    list = Friend.objects.all()
    if request.method == 'POST':
        for var in list:
            if var.friend_one.username == request.POST.get('my_name'):
                friend = {}
                friend['name'] = var.friend_other.username
                friend['headImg'] = var.friend_other.headImg.__str__().split('./uploads/')[1]
                friend['isOnline'] = var.friend_other.isOnline
                friends.append(friend)
    import json
    return HttpResponse(json.dumps(friends))  # 返回user数据给安卓端


def add_dynamic(request):
    if request.method == 'POST':
        if request.FILES:
            # 有图片上传
            kwargs = {
                'username': request.POST['username'],
                'context': request.POST['context'],
                'img': request.FILES.get('file')
            }
            dynamic = Dynamic.objects.create(**kwargs)
            dynamic.save()
            return HttpResponse('success')
        else:
            # 无图片上传
            dynamic = Dynamic.objects.create(username=request.POST['username'], context=request.POST['context'])
            dynamic.save()
            return HttpResponse('success')
    else:
        return HttpResponse('method error')


def get_all_dynamic(request):
    dynamics = []
    friends = []
    dynamicList = Dynamic.objects.all()
    friendList = Friend.objects.all()
    username = request.POST.get('username')

    if request.method == 'POST':
        for var in friendList:
            if var.friend_one.username == username:
                friends.append(var.friend_other.username)
        friends.append(username)
        for var in dynamicList:
            if var.username in friends:
                dynamic = {}
                dynamic['username'] = var.username
                dynamic['context'] = var.context
                dynamic['time'] = var.c_time.__str__()
                if var.img.__str__() == '':
                    dynamic['image'] = var.img.__str__()
                else:
                    dynamic['image'] = var.img.__str__().split('uploads/')[1]
                temp_user = MyUser.objects.get(username=var.username)
                dynamic['headImage'] = temp_user.headImg.__str__()
                dynamic['headImage'] = temp_user.headImg.__str__().split('uploads/')[1]
                dynamics.append(dynamic)
        return HttpResponse(json.dumps(dynamics))
    return HttpResponse('none')


def delete_dynamic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        time = request.POST.get('time')
        Dynamic.objects.filter(username=username, c_time=time).delete()
        return HttpResponse('success')


def change_head_image(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        kwargs = {
            'username': username,
            'headImg': request.FILES.get('file'),
        }

        # user = MyUser.objects.filter(username=username)
        # user.update(**kwargs)
        print(username)
        print(request.FILES)
        return HttpResponse('success')
    else:
        return HttpResponse('failed')
