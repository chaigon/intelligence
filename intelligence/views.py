# coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from forms import BaseForm
from django.http import JsonResponse
import common
import action


@csrf_exempt
@common.json_dumps(ensure_ascii=True)
def home(request):
    params = getattr(request, request.method, '')

    if not params:
        import json
        params = json.loads(request.body)

    form = BaseForm(params)
    form.is_valid()
    cld = form.cleaned_data
    do_action = cld.get('action')  # 功能函数名
    # user_id = cld.get('user_id')  # 用户名在数据库的id

    if not do_action:
        context = {
            'return_code': -1,
            'message': u'系统异常。'
        }
        return JsonResponse(context)
    func = getattr(action, do_action, None)

    setattr(request, 'action', do_action)
    return_data = func(request)

    args = request.POST.keys()
    values = request.POST.values()
    log = ''
    for index, k in enumerate(args):
        log += k + '=' + values[index] + '&'
    # if isinstance(return_data, dict):
    #    logger.info(log[0: -1] + ',' + str(return_data['return_code']))
    return return_data
