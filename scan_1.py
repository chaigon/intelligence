# coding:utf-8

import postfile

Public_ApiKey = '508658e4e66e4aeba23b8da1f39b75785feaa35d442e4957a311f64d0613a267'


def scan_file():
    host = "x.threatbook.cn"
    selector = "https://x.threatbook.cn/api/v1/file/scan"
    fields = [("apikey", Public_ApiKey)]
    file_content = open("sess201708090954.csv", "rb").read()
    files = [("file", "sess201708090954.csv", file_content)]
    json = postfile.post_multipart(host, selector, fields, files)
    print json
    return json


def get_report():
    import json as simplejson
    import urllib
    import urllib2
    url = "https://x.threatbook.cn/api/v1/file/report"
    parameters = {'apikey': Public_ApiKey,
                  'resource': '48735df1a39daa53d3de806c6d2c0d78fe5ab817c5831d73c9b79c9782a3c3fa'}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json = response.read()
    print json


if __name__ == "__main__":
    # scan_file()
    get_report()
