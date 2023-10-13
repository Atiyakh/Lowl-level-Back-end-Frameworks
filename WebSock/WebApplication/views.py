from MiddleWare.Views import HTTPResponse, ImportStatic, ImportMedia

class Application1():
    def login_style(req):
        return HTTPResponse(ImportStatic("css/login-style.css"))
    def home_page(req):
        return HTTPResponse(ImportStatic("html/home_page.html"))
    def about_us(req):
        return HTTPResponse(ImportStatic("html/about-us.html"))
    def contact_us(req):
        return HTTPResponse(ImportStatic("html/contact-us.html"))
    def login(req):
        if req.method == 'POST':
            pass
        else:
            return HTTPResponse(ImportStatic("html/login-page.html"))
    def image1(req):
        return HTTPResponse(ImportMedia("favicon.jpg"))
    def favicon(req):
        return HTTPResponse(ImportMedia("Media_1/favicon.ico"))
