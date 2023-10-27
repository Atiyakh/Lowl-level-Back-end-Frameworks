import traceback, json
from urllib.parse import parse_qs
import time, sqlite3 as sql
import pathlib, os

class HttpRequest:
    def __init__(self, method, url, http_version, headers, payload, peername):
        self.url = url
        self.method = method
        self.headers = headers
        if 'Cookie' in self.headers:
            self.raw_cookies = self.headers['Cookie']
        else: self.raw_cookies = ''
        if self.raw_cookies:
            print(self.raw_cookies)
            self.cookies = {key: val for key, val in [cookie.split('=', 1) for cookie in self.raw_cookies.split('; ')]}
        else: self.cookies = dict()
        if 'session' in self.cookies: self.session = self.cookies['session']
        else: self.session = None
        self.http_version = http_version
        self.payload = payload
        self.remote_peername = peername
        self.remote_ip = self.remote_peername[0]
        if self.session:
            ApplicationDB = sql.connect(os.path.join(pathlib.Path(__file__).parent, "Database\\sqlite3.db"))
            cur = ApplicationDB.cursor()
            try: cur.execute("SELECT username, password, email, first_name, last_name, authentication FROM auth_websock_default_user_table WHERE authentication=?", (self.session,))
            except sql.IntegrityError:
                cur.close()
                ApplicationDB.close()
                return False
            query = cur.fetchone()
            ApplicationDB.commit()
            cur.close()
            ApplicationDB.close()
        else: query = False
        if query:
            rows = ['username', 'password', 'email', 'first_name', 'last_name', 'authentication']
            self.user_creditentials = {rows[num]: query[num] for num in range(len(rows))}
            self.authenticated_user = True
        else:
            self.user_creditentials = None
            self.authenticated_user = False
        self.remote_port = self.remote_peername[1]

async def request_processor_(request, peername, views):
    try:
        try:
            request_headers, request_payload = request.decode('utf-8').split("\r\n\r\n")
        except:
            if not request:
                print('[WebSock] Empty request.')
        request_headers = request_headers.splitlines()
        method, url, http_version = request_headers[0].split(' ')
        headers_format = '{\n'
        for line in request_headers[1:]:
            key, val = line.split(':', 1)
            val = val.replace('"', '\\"')
            if line == request_headers[1:][-1]: headers_format += f'''"{key}": "{val[1:]}"\n'''
            else: headers_format += f'''"{key}": "{val[1:]}",\n'''
        headers_format += '}'
        headers = json.loads(headers_format)
        url_query_p = parse_qs(request_payload)
        url_query_parsed = {key: val[0] for key, val in url_query_p.items()}
        req = HttpRequest(method, url, http_version, headers, url_query_parsed, peername)
        print(f"[WebSock] {method} Request - {url} - {time.ctime()}")
        try:
            view_function = URLRouting.RetrieveView(url)
            if view_function:
                processed_request = view_function(req)
                if type(processed_request).__name__ == 'coroutine':
                    processed_request = await processed_request
                return processed_request
            else:
                print(f"[WebSock] {req.url} - Not Found 404 - {time.ctime()}")
                if 'NotFound404' in dir(views):
                    return views.NotFound404(req)
        except:
            traceback.print_exc()
            print('[WebSock] Request processing failure.')
    except:
        traceback.print_exc()
        print('[WebSock] Request processing failure.')
import sys
sys.path.append(r"C:\Users\skhodari\Desktop\ATTYA\WebSock V2\WebApplication")
from MiddleWare.Routing import URLRouting
