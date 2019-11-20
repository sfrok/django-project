"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from baseapp import views
from .data import HtmlPages as HP

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=f'{HP.home}_page'),
    path(f'{HP.reg}/', views.reg_view, name=f'{HP.reg}_page'),
    path(f'{HP.auth}/', views.auth_view, name=f'{HP.auth}_page'),

    path(f'{HP.srch_inp}/', views.search_input_view, name=f'{HP.srch_inp}_page'),
    path(f'{HP.srch_res}/', views.search_result_view, name=f'{HP.srch_res}_page'),

    re_path(r'(product/)(\d+)', views.product_view, name=f'{HP.product}_page'),
    path(f'{HP.ord}/', views.order_view, name=f'{HP.ord}_page'),
    path(f'{HP.ord_com}/', views.order_complete_view, name=f'{HP.ord_com}_page'),
    path(f'{HP.ord_list}/', views.order_list_view, name=f'{HP.ord_list}_page'),

    path(f'{HP.settings}/', views.settings_view, name=f'{HP.settings}_page'),
    path(f'{HP.contacts}/', views.contacts_view, name=f'{HP.contacts}_page'),

    path(f'edit/', views.edit_all_view, name=f'{HP.edit_all}_page'),
    path(f'edit/orders/', views.edit_bst_view, name=f'{HP.edit_bst}_page'),
    path(f'edit/categories/', views.edit_cat_view, name=f'{HP.edit_cat}_page'),
    path(f'edit/products/', views.edit_prd_view, name=f'{HP.edit_prd}_page'),
    path(f'edit/users/', views.edit_usr_view, name=f'{HP.edit_usr}_page'),
    re_path(r'(edit/orders/)(\d+)', views.add_bst_view, name=f'{HP.add_bst}_page'),
    re_path(r'(edit/categories/)(\d+)', views.add_cat_view, name=f'{HP.add_cat}_page'),
    re_path(r'(edit/products/)(\d+)', views.add_prd_view, name=f'{HP.add_prd}_page'),
    re_path(r'(edit/users/)(\d+)', views.add_usr_view, name=f'{HP.add_usr}_page'),
]

if settings.DEBUG:
    # only serves the actual STATIC_ROOT folder
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
