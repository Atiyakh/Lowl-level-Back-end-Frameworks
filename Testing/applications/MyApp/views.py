from InfraWeb.MiddleWare.Views import HttpResponse, InsertValues, Template, ImportStatic
import time

def WelcomePage(request):
    return HttpResponse(Template("Ayyy, what up {{username}} ({{date}})"), InsertValues(
        username="Mohammad", date=time.ctime()
    ), request)
