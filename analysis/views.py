# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import urllib
import urllib2
import json
import re
from django.http import JsonResponse
from analysis import forms
from django.conf import settings
# Create your views here.
from django.http import StreamingHttpResponse


def analysis(request):
    """
    分析数据
    :param request:
    :return:
        datalist = {
                name: '赵成',
                draggable: true,
            }, {
                name: '陈现忠',
                draggable: true,
            }, {
                name: '陶泳',
                category: 1,
                draggable: true,
            },
            linklist = [{
                source: 1,
                target: 2,
                value: ''
            }, {
                source: 0,
                target: 5,
                value: ''
            }]
    """
    params = getattr(request, request.method)
    if not params:
        params = json.loads(request.body)
    form = forms.AnalysisForm(params)
    if not form.is_valid():
        return_data = {
            'return_code': 3,
            'message': u'参数错误。'
        }
        return return_data
    cld = form.cleaned_data
    domain = cld['domain_ip'].strip()
    data_list = []
    link_list = []
    # 判断是域名还是IP
    pattern = re.compile(r"((?:(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d))\.){3}(?:25[0-5]|2[0-4]\d|(?:1\d{2}|[1-9]?\d)))")
    match = pattern.match(domain)
    if match:
        parameters = {"ip": match.group(), "apikey": settings.API_KEY,
                      "field": " tags, judgments,  asn, samples, intelligences, ip"}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(settings.THREAT_BOOK_IP_URL, data)
        response = urllib2.urlopen(req)
        ret_json = json.loads(response.read())
        samples = ret_json.setdefault('samples', [])
        for sample in samples:
            data_list.append({"name": sample['sha256'], "category": 1, "draggable": True})
        data_list.append({"name": domain, "draggable": True})
        main_index = data_list.index({"name": domain, "draggable": True})
        for index, value in enumerate(data_list):
            if value.get('category', 0):
                link_list.append({"source": index, "target": main_index, "value": ''})
    else:
        parameters = {"domain": domain, "apikey": settings.API_KEY,
                      "field": "cur_ips, cur_ips.location, cur_whois, tags, domains_4_name,domains_4_email,judgments"}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(settings.THREAT_BOOK_DOMAIN_URL, data)
        response = urllib2.urlopen(req)
        ret_json = json.loads(response.read())

        domains_4_names = ret_json.setdefault('domains_4_name', [])
        # print "domains_4_names..", domains_4_names
        cur_whois = ret_json.setdefault('cur_whois', {})
        cur_ips = ret_json.setdefault('cur_ips', [])
        domain = ret_json['domain']
        main_index = 0

        for domains_4_name in domains_4_names:
            data_list.append({"name": domains_4_name, "category": 1, "draggable": True})
        if cur_whois.get('registrant_name', None):
            data_list.append({"name": cur_whois['registrant_name'], "draggable": True})
            main_index = data_list.index({"name": cur_whois['registrant_name'], "draggable": True})
        data_list.append({"name": domain, "draggable": True})
        domain_index = data_list.index({"name": domain, "draggable": True})

        for index, value in enumerate(data_list):
            if value.get('category', 0):
                if cur_whois.get('registrant_name', None):
                    link_list.append({"source": index, "target": main_index, "value": ''})
                else:
                    link_list.append({"source": index, "target": domain_index, "value": ''})
        link_list.append({"source": domain_index, "target": main_index, "value": ''})
        if cur_whois.get('registrant_email', None):
            data_list.append({"name": cur_whois['registrant_email'], "category": 1, "draggable": True})
            email_index = data_list.index({"name": cur_whois['registrant_email'], "category": 1, "draggable": True})
            link_list.append({"source": email_index, "target": domain_index, "value": ''})

        for cur_ip in cur_ips:
            data_list.append({"name": cur_ip['ip'], "category": 1, "draggable": True})
            ip_index = data_list.index({"name": cur_ip['ip'], "category": 1, "draggable": True})
            link_list.append({"source": ip_index, "target": domain_index, "value": ''})

    context = {
        "status": 0,
        "message": u"查询成功",
        "data_list": data_list,
        "link_list": link_list

    }
    return JsonResponse(context)


def down_work_table_bak(request):
    """
    下载工作表
    :param request:
    :return:
    """
    user = request.user
    # form = forms.DownWorkTableForm(getattr(request, request.method))
    # if not form.is_valid():
    #     return_data = {
    #         'return_code': 3,
    #         'message': u'参数错误。'
    #     }
    #     return return_data
    # cld = form.cleaned_data
    #
    # work_table_ids = cld['work_table_ids']
    # work_table_id_list = work_table_ids.split(',')
    #
    # work_table_set = WorkTable.objects.filter(id__in=work_table_id_list).values("work_table_uuid", "work_table_rename")
    work_table_set = [{"work_table_uuid": '362325c5-6ac1-11e7-8fca-f45c89a97b13.csv',
                       'work_table_rename': 'change_work_table_name'}]

    # file_dir = settings.WORKTABLE_TEMPLATE_PATH + "user_{}/".format(user.id)
    file_dir = '/data/test_django/store/'
    for work_table in work_table_set:
        # file_path = os.path.join(file_dir, work_table['work_table_uuid'])
        file_path = '/data/test_django/store/' + work_table['work_table_uuid']

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        the_file_name = work_table['work_table_rename'] + ".csv"
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

        return response


import csv
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
class Echo(object):
	"""An object that implements just the write method of the file-like
	interface.
	"""
	def write(self, value):
		"""Write the value by returning it, instead of storing in a buffer."""
		return value
def down_work_table(request):
	"""A view that streams a large CSV file."""
	# Generate a sequence of rows. The range is based on the maximum number of
	# rows that can be handled by a single sheet in most spreadsheet
	# applications.
	rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))
	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)
	response = StreamingHttpResponse((writer.writerow(row) for row in rows),
									 content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
	return response