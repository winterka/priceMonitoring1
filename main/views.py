from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Ну собсна страница как она есть")