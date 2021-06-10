from django.shortcuts import render
from .models import Complete
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index(request):
    chart_elements = {'chart_elements': list(Complete.objects.values())}
    return render(request, 'main/index.html', chart_elements)

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

def link(request):
    return render(request, 'main/link.html')
