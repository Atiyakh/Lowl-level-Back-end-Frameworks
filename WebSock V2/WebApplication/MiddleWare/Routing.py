import time, sys, os, traceback
from Views import HttpResponse, ImportMedia, ImportStatic
from urllib.parse import urlparse, parse_qs

# Custom routing system with direct static and media 
# routing, facilitated template processing, and easy
# views-based assets importation.
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

def enhanced_response_generation(path, route, query, param, req):
    req.url_query = query
    req.param = param
    req.path = path
    return route(req, **param)

class ArgumentURL(list):
    def __init__(self, view_function):
        self.view_function = view_function
    def add_fragment(self, fragment):
        self.append(fragment)
    def compare_urls(self, url):
        url_fragments = url.split('/')[1:]
        args_dictionary = dict()
        if len(url_fragments) == len(self):
            valid = True
            for fragment_number in range(len(self)):
                if not (self.__getitem__(fragment_number) == url_fragments[fragment_number]):
                    valid = False
                elif type(self.__getitem__(fragment_number)).__name__ == 'FragmentArgumentURL':
                    args_dictionary[self.__getitem__(fragment_number).arg_name] = url_fragments[fragment_number]
            if valid: return self.view_function, args_dictionary
            else: return False
        else: return False

class FragmentArgumentURL:
    def __eq__(self, __value:str):
        val_type = 'str'
        if __value.isnumeric():
            val_type = 'int'
        elif (len(__value.split('.')) == 2):
            if (__value.split('.')[0].isnumeric()) and (__value.split('.')[1].isnumeric()):
                val_type = 'float'
        if val_type == self.arg_type: return True
        else: return False
    def __init__(self, arg_type, arg_name):
        self.arg_type = arg_type
        self.arg_name = arg_name

class Routing:
    def __init__(self):
        self.urls = dict()
        self.arg_urls = []
    def seek_argument_urls(self, url):
        for arg_url in self.arg_urls:
            result = arg_url.compare_urls(url)
            if result: return result
    def parse_argument(self, url, view_function):
        is_arg = False
        url_fragments = []
        fragments = url.path.split('/')[1:]
        for fragment_number in range(len(fragments)):
            fragment = fragments[fragment_number]
            if (fragment[0] == '<') and (fragment[-1] == '>'):
                is_arg = True
                arg_cmd = fragment[1:-1]
                if ':' in arg_cmd:
                    arg_type, arg_name = arg_cmd.split(':')
                    if arg_type in ['str', 'int', 'float']:
                        url_fragments.append(FragmentArgumentURL(
                            arg_type=arg_type,
                            arg_name=arg_name
                        ))
                else: raise SyntaxError(
                    "[WebSock] Invalid argument URL syntax."
                )
            else: url_fragments.append(fragment)
        if is_arg:
            argument_url = ArgumentURL(view_function)
            for fragment in url_fragments:
                argument_url.add_fragment(fragment)
            self.arg_urls.append(argument_url)

    def Structure(self, *urls):
        for url in urls:
            if isinstance(url, MEDIA):
                for file in url.files:
                    self.urls[f"{url.path}/{file}"] = url.media_route_parser
            elif isinstance(url, URL):
                self.urls[url.path] = url.application_view
                self.parse_argument(url, url.application_view)
            else:
                print(f"- Warning: Route ({url}) is not a URL nor MEDIA   [ROUTE IGNORED]")
    def RetrieveView(self, url):
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
                url_query = {key: val for key, val in parse_qs(url_parsed.query).items()}
                try:
                    url_route = self.urls[url_path]
                    return lambda req: enhanced_response_generation(
                        path=url_path, route=url_route,
                        query=url_query, param={}, req=req
                    )
                except KeyError:
                    arg_url = self.seek_argument_urls(url)
                    if arg_url:
                        return lambda req: enhanced_response_generation(
                            path=url_path, route=arg_url[0],
                            query=url_query, param=arg_url[1], req=req
                        )
                    else: return False
            
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
