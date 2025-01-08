from MiddleWare.Views import HttpResponse, InsertValues, ImportStatic, ImportMedia, redirect, render, login_needed, verify_csrf
from MiddleWare.Database.Models import Where
import models
from MiddleWare.auth import MiddleWare_Default_Models

User = MiddleWare_Default_Models.User()
Student = models.Student()

print(Student.fields)

def csrf_exception(request):
    return HttpResponse("You provided an invalid CSRF token. unfortunately, we can't let you in ):")

@login_needed
async def profile(request, username):
    return render(
        request,
        'html/profile.html',
        {
            'username': username,
        },
        content_type="application/xhtml+xml"
    )

@verify_csrf
async def login(request):
    if request.method == 'POST':
        username = request.payload['username']
        password = request.payload['password']
        if User.login_user(request, username=username, password=password):
            return redirect(request, f'/{username}/profile')
        else:
            return render(request, 'html/login-page.html')
    else:
        return render(request, 'html/login-page.html')

@verify_csrf
async def signup(request):
    if request.method == 'POST':
        request
        username = request.payload['username']
        password = request.payload['password']
        if User.create_user(request, username=username, password=password):
            return redirect(request, f'/{username}/profile')
        else:
            return render(request, 'html/signup-page.html')
    else:
        return render(request, 'html/signup-page.html')

async def home_page(request):
    return render(request, "html/home_page.html")

async def about_us(request):
    return render(request, "html/about-us.html")

async def contact_us(request):
    return render(request, "html/contact-us.html")

async def favicon(request):
    return HttpResponse(ImportMedia("Media_1/favicon.ico"), request)
