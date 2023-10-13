from MiddleWare.Routing import URLRouting, URL, MEDIA
import views

URLRouting.Structure(
    URL("/", views.Application1.home_page),
    URL("/contact-us", views.Application1.contact_us),
    URL("/login", views.Application1.login),
    URL("/login-style.css", views.Application1.login_style),
    URL("/about-us", views.Application1.about_us),
    URL("/favicon.ico", views.Application1.favicon),
    MEDIA("/images-store-1", "Media_1")
)
