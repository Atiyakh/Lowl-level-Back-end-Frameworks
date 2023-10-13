import traceback

class Request:
    def __init__(self, method, url, http_version):
        self.url = url
        self.method = method
        self.http_version = http_version

def request_processor_(request):
    try:
        request_format = request.decode('utf-8').splitlines()
        method, url, http_version = request_format[0].split(' ')
        req = Request(method, url, http_version)
        return URLRouting.RetrieveView(url)(req)
    except:
        traceback.print_exc()

import sys
sys.path.append(r"C:\Users\skhodari\Desktop\ATTYA\WebSock\WebApplication")
from MiddleWare.Routing import URLRouting
