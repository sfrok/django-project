from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm


def home(request):
    return HttpResponse("<html><body>Hello World!</body></html>")


def home2(request):
    return render(request, 'home2.html', {})


def registration_form(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        return HttpResponseRedirect(reverse('home'))
    context = {
        'form': form
    }
    return render(request, 'registaration.html', context)





