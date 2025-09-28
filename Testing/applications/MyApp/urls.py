from InfraWeb.MiddleWare.Routing import Mapping, URL, MEDIA, STATIC
import views

# bind your views and media directories to their proper urls

URLMapping = Mapping()
URLMapping.Structure(
    URL("/", views.WelcomePage),
    URL("/favicon.ico", views.favicon)
)
