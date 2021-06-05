from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/index.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('./')
    else:
        return HttpResponseRedirect('/account/invalid')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("./")
