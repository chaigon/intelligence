import httplib, mimetypes
import urllib
import urllib2
import os
import sys
import optparse
import hashlib
import time

# The apikey
API_KEY = "9b3b63d3d9f841928c17a7981453c0cec8592d420fd64a808a81acb09a8ecc66"


class ThreatBook(object):
    def __init__(self, api_key):
        super(ThreatBook, self).__init__()
        self.api_key = api_key

    def __repr__(self):
        return "<ThreatBook proxy>"

    def get(self, ip):
        print "Getting the result ...\r\n"

        url = "https://x.threatbook.cn/api/v1/ip/query"
        # url = "http://localhost:9000/api/v1/ip/query"
        parameters = {"ip": ip, "apikey": self.api_key, "field": "domains"}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        ret_json = response.read()
        print "Report(in JSON):\r\n"
        print ret_json
        return 1


def main():
    parser = optparse.OptionParser(usage = """
    %prog <ip>
Samples:
    %prog 82.165.37.26
    """)

    (options, arguments) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        return -1

    ip = arguments.pop(0)
    try:
        v = ThreatBook(API_KEY)
        v.get(ip)

    except Exception, e:
        print "ThreatBook returned a non correct response."

if __name__ == "__main__":
    main()