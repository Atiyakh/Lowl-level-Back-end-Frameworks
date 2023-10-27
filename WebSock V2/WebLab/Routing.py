import time, sys, os, traceback
from Views import HttpResponse, ImportMedia, ImportStatic
from urllib.parse import urlparse, parse_qs

media_path = r"WebApplication\assets\media"

class MEDIA:
    def __init__(self, path, media_dir):
        if '/' in media_dir or '\\' in media_dir:
            raise ValueError("[WebSock] invalid media_path value")
        self.media_dir = media_dir
        self.path = path
        self.files = os.listdir(os.path.join(media_path, media_dir))
    def media_route_parser(self, req):
        file = os.path.join(self.media_dir, req.url.split('/')[-1])
        return HttpResponse(ImportMedia(file))

def response_generation(path, route, query, param, req):
    req.payload = query
    req.param = param
    req.path = path
    return route(req)

class Routing:
    def __init__(self):
        self.urls = dict()
    def Structure(self, *urls):
        for url in urls:
            if isinstance(url, MEDIA):
                for file in url.files:
                    self.urls[f"{url.path}/{file}"] = url.media_route_parser
            elif isinstance(url, URL):
                self.urls[url.path] = url.application_view
            else:
                print(f"- Warning: Route ({url}) is not a URL nor MEDIA   [ROUTE IGNORED]")
    def RetrieveView(self, url):  # TODO [param]
        try:
            if url.split('/')[1] == 'media':
                path_ = url[url.find('/media/')+7:]
                return lambda _: HttpResponse(ImportMedia(path_))
            elif url.split('/')[1] == 'static':
                path_ = url[url.find('/static/')+8:]
                return lambda _: HttpResponse(ImportStatic(path_))
            else:
                url_parsed = urlparse(url)
                url_path = url_parsed.path
                if url_path[-1] in '\\/': url_path = url_path[:-1]
                url_query = url_parsed.query
                print(url_path)
                url_route = self.urls[url_path]
                print(f"[WebSock] GET Request - {url} - {time.ctime()}")
                return lambda req: response_generation(
                    path=url_path, route=url_route,
                    query=url_query, param=None, req=req
                )
        except:
            traceback.print_exc()
            print(f"[WebSock] GET Request - {url} - page not avaliable - {time.ctime()}")
            sys.exit()

class URL:
    def __init__(self, path, view):
        if path[-1] in '\\/': path = path[:-1]
        self.path = path
        self.application_view = view

URLRouting = Routing()
import urls
