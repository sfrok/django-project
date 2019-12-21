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
    path(f'{HP.out}/', views.logout_view, name=f'{HP.out}_page'),
    path('activate/<str:uid>/<str:token>', views.activation_view, name='activation_page'),

    path(f'{HP.prd}/', views.search_view, name=f'{HP.src}_page'),
    re_path(r'(products/)(\d+)', views.product_view, name=f'{HP.prd}_page'),
    path(f'{HP.ord}/', views.order_view, name=f'{HP.ord}_page'),
    path(f'{HP.ord_add}/', views.order_add_view, name=f'{HP.ord_add}_page'),
    path(f'{HP.ord_del}/', views.order_del_view, name=f'{HP.ord_del}_page'),
    path(f'{HP.ord}/{HP.ord_com}/', views.order_complete_view, name=f'{HP.ord_com}_page'),

    path(f'{HP.cab}/', views.cabinet_view, name=f'{HP.cab}_page'),
    path(f'{HP.contacts}/', views.contacts_view, name=f'{HP.contacts}_page'),
]

handler404 = 'baseapp.views.not_found'

if settings.DEBUG:  # only serves the actual STATIC_ROOT folder
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
