from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Product, Basket, Category
from baseapp.scripts import HtmlPages, session_clear

@session_clear
def edit_all_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.edit_all}.html')
    else: return HttpResponseRedirect('/')


@session_clear
def edit_bst_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.edit_bst}.html', {'baskets': Basket.objects.all()})
    else: return HttpResponseRedirect('/')


@session_clear
def edit_cat_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.edit_cat}.html', {'cats': Category.objects.all()})
    else: return HttpResponseRedirect('/')


@session_clear
def edit_prd_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.edit_prd}.html', {'products': Product.objects.all()})
    else: return HttpResponseRedirect('/')


@session_clear
def add_bst_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.add_bst}.html', {'baskets': Basket.objects.all()})
    else: return HttpResponseRedirect('/')


@session_clear
def add_cat_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.add_cat}.html', {'cats': Category.objects.all()})
    else: return HttpResponseRedirect('/')


@session_clear
def add_prd_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.add_prd}.html', {'products': Product.objects.all()})
    else: return HttpResponseRedirect('/')
