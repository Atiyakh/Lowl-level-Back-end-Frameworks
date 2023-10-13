import time, sys, os
from Views import HTTPResponse, ImportMedia

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
        return HTTPResponse(ImportMedia(file))

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
    def RetrieveView(self, url):
        try:
            route = self.urls[url]
            print(f"[WebSock] GET Request - {url} - {time.ctime()}")
            return route
        except:
            print(f"[WebSock] GET Request - {url} - page not avaliable - {time.ctime()}")
            sys.exit()

class URL:
    def __init__(self, path, view):
        self.path = path
        self.application_view = view

URLRouting = Routing()
import urls
