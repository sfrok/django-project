from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Product, Basket, Category
from .forms import AdminCatForm
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
        if request.method == 'POST' and 'edit_cat_id' in request.session:
            form = AdminCatForm(request.POST)
            if form.is_valid():
                if request.session['edit_cat_id'] == 0:
                    Category.objects.create(name=form.cleaned_data['name'])
                else:
                    c = Category.objects.get(id=request.session['edit_cat_id'])
                    c.name = form.cleaned_data['name']
                    c.save()
                del request.session['edit_cat_id']
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
        cat_id = int(request.path[17:])
        if cat_id != 0: cat = Category.objects.get(id=cat_id).name
        else: cat = ''
        request.session['edit_cat_id'] = cat_id
        return render(request, f'{HtmlPages.add_cat}.html', {'cat':cat})
    else: return HttpResponseRedirect('/')


@session_clear
def add_prd_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, f'{HtmlPages.add_prd}.html', {'cats': Category.objects.all()})
    else: return HttpResponseRedirect('/')
