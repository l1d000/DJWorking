from django.shortcuts import render
from django.http import HttpResponse  
from  pytools.tool_shell import shell_command
from django.contrib import auth
from models import BuildProject
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
import rom_build

# Create your views here.
def index(request):
    context          = {}
    context['title'] = 'Hello World!'
    project_names = BuildProject.objects.all()
    context['project_names'] = project_names
    for i in project_names:
        print(i.project_Name)
    context['username'] = 'Hello World!'
    if  request.user.is_authenticated():
        return render(request, 'index.html', context)
    else:
        return render(request, 'login.html', context)

def running(request):
    context ={}
    if  request.user.is_authenticated():
       context = {
           'username': request.user.username
       }
    else:
        return render(request, 'login.html', context)
       
    if rom_build.get_running_status() :
       print("running")
       context['title'] = rom_build.get_running_project()
       context['username'] = request.user.username  
       return render(request, "sync.html", context)
    if request.POST:
        print(request.POST['project_name'])
        #print(request.POST['cl_number'])
        if rom_build.rom_running(request.POST['project_name']):
            return render(request, "sync.html", context)
        
    context['title'] = 'Hello World! Please try again!'
    project_names = BuildProject.objects.all()
    context['project_names'] = project_names
    return render(request, "index.html", context)

@csrf_exempt
def login_user(request):
    if  request.user.is_authenticated():
        context = {
                    'username': request.user.username
                }
        return render(request, 'index.html', context)

    if request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None:  
            if user.is_active:  
                login(request, user)
                context = {
                    'username': request.user.username
                }
                return render(request, 'index.html', context)
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else: 
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
   # form = UserForm(request.POST or None)
   # context = {
   #     "form": form,
   # }
    context          = {}
    context['username'] = 'Hello World!'
    return render(request, 'login.html', context)

def animation(request):
    context          = {}
    return render(request, 'animation.html', context)

def base(request):
    context          = {}
    return render(request, 'base.html', context)

def default(request):
    context          = {}
    return render(request, 'default.html', context)

def test(request):
    context          = {}
    shell_command("cd /home/lidongzhou/HTC/work/test;find -name *.txt")
    return render(request, 'default.html', context)
