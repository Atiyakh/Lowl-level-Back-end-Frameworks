from MiddleWare.Views import HttpResponse, InsertValues, ImportStatic, ImportMedia, redirect, render, login_needed
from MiddleWare.Database.Models import Where
from models import Teacher
from MiddleWare.auth import MiddleWare_Default_Models

User = MiddleWare_Default_Models.User()
Teacher = Teacher()

def NotFound404(request):
    return redirect(request, '/login')

@login_needed
def profile(request, username):
    print(request.headers)
    return render(
        request,
        'html/profile.html',
        {
            'username': username,
        },
        content_type="application/xhtml+xml"
    )

async def login(request):
    if request.method == 'POST':
        username = request.payload['username']
        password = request.payload['password']
        if User.login_user(request, username=username, password=password):
            print('loged in')
            return redirect(request, f'/{username}/profile')
        else:
            print('unable to login')
            return render(request, 'html/login-page.html')
    else:
        return render(request, 'html/login-page.html')

async def signup(request):
    if request.method == 'POST':
        request
        username = request.payload['username']
        password = request.payload['password']
        if User.create_user(request, username=username, password=password):
            print('signed up')
            return redirect(request, f'/{username}/profile')
        else:
            print('unable to signup')
            return render(request, 'html/signup-page.html')
    else:
        return render(request, 'html/signup-page.html')

def home_page(request):
    return render(request, "html/home_page.html")

def about_us(request):
    return render(request, "html/about-us.html")

def contact_us(request):
    return render(request, "html/contact-us.html")

def favicon(request):
    return HttpResponse(ImportMedia("Media_1/favicon.ico"), request)
