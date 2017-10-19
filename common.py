
# coding:utf-8

import json
from django.http import HttpResponse


def json_dumps(ensure_ascii=True):
    """
    Dumps json data.
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            try:
                output_dumps = json.dumps(output, ensure_ascii=ensure_ascii)
            except:
                return HttpResponse(output)

            response = HttpResponse(output_dumps)

            response['X-Frame-Options'] = '*'
            response['Access-Control-Allow-Origin'] = '*'

            response.cookies['username'] = request.user.username
            response.cookies['user_id'] = request.user.id
            response.set_cookie(key='username',
                                value=request.user.username,
                                max_age=60 * 60 * 24 * 7 * 52,
                                )
            response.set_cookie(key='user_id',
                                value=request.user.id,
                                max_age=60 * 60 * 24 * 7 * 52,
                                )
            return response
        return wrapper
    return decorator


def my_login_required(function):
    """
    判断用户是否登录
    :param function:
    :return:
    """
    def wrapper(request, *args, **kw):
        if request.user and request.user.is_authenticated():
            return function(request, *args, **kw)
        else:
            return HttpResponse(status=401)
    return wrapper


