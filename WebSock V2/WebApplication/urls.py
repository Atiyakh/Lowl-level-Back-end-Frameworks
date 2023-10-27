from MiddleWare.Routing import URLRouting, URL, MEDIA
import views

URLRouting.Structure(
    URL("/", views.home_page),
    URL("/login", views.login),
    URL("/signup", views.signup),
    URL("/<str:username>/profile", views.profile),
    URL("/contact-us", views.contact_us),
    URL("/about-us", views.about_us),
    URL("/favicon.ico", views.favicon),
    MEDIA("/images-store-1", "Media_1"),
)