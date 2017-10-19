# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def my_login(request):

    if request.method == 'GET':
        print request.body
        username = request.GET.get('username').strip()
        password = request.GET.get('password').strip()
    elif request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
    else:
        username = ''
        password = ''
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            context = {
                "return_code": 0,
                'message': u'登录成功。',
                'data': {
                    "user_id": user.id
                }
            }
        else:
            context = {
                "return_code": 301,
                'message': u'用户不存在。'
            }
    else:
        context = {
            "return_code": 4,
            'message': u'用户名或密码错误。'
        }
    return JsonResponse(context)


def my_logout(request):
    logout(request)
    context = {
        "return_code": 0,
        'message': u'退出成功。'
    }
    return JsonResponse(context)
