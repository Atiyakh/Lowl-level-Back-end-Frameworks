from importlib.machinery import SourceFileLoader
import os, pathlib
Routing = SourceFileLoader("Routing", os.path.join(pathlib.Path(__file__).parent, 'MiddleWare\\Routing.py')).load_module()
auth = SourceFileLoader("auth", os.path.join(pathlib.Path(__file__).parent, 'MiddleWare\\auth.py')).load_module()
URLRouting = Routing.URLRouting
URL = Routing.URL
MEDIA = Routing.MEDIA
admin = auth.admin
views = SourceFileLoader("views", os.path.join(pathlib.Path(__file__).parent, 'views.py')).load_module()

# bind your view functions to their suitable URLs.

URLRouting.Structure(
    URL("/", views.home_page),
    URL("/admin", admin),
    URL("/login", views.login),
    URL("/signup", views.signup),
    URL("/<str:username>/profile", views.profile),
    URL("/contact-us", views.contact_us),
    URL("/about-us", views.about_us),
    URL("/favicon.ico", views.favicon),
    MEDIA("/images-store-1", "Media_1"),
)
