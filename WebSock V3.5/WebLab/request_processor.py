import traceback, json

class Request:
    def __init__(self, method, url, http_version, headers, payload):
        self.url = url
        self.method = method
        self.headers = headers
        self.http_version = http_version
        self.payload = payload

def request_processor_(request):
    try:
        request_headers, payload = request.decode('utf-8').split("\r\n\r\n")
        request_headers = request_headers.splitlines()
        method, url, http_version = request_headers[0].split(' ')
        headers_format = '{\n'
        for line in request_headers[1:]:
            key, val = line.split(':', 1)
            if line == request_headers[1:][-1]: headers_format += f'''"{key}": "{val[1:]}"\n'''
            else: headers_format += f'''"{key}": "{val[1:]}",\n'''
        headers_format += '}'
        headers = json.loads(headers_format)
        req = Request(method, url, http_version, headers, payload)
        try:
            processed_rquest = URLRouting.RetrieveView(url)(req)
            return processed_rquest
        except:
            traceback.print_exc()
            print('[WebSock] Processing request failed.')
    except:
        traceback.print_exc()

import sys
sys.path.append(r"C:\Users\skhodari\Desktop\ATTYA\WebSock\WebApplication")
from MiddleWare.Routing import URLRouting
