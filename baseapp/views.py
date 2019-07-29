from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("<html><body>Hello World!</body></html>")


def home2(request):
    return render(request, 'home2.html', {})



