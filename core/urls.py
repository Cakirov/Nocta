"""core URL Configuration

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
    2. Add a URL to urlpatterns:  path('nocta/', include('nocta.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blog.views import (
    index, post_detail, category_show,
    register, user_login, contact_view,
    search_results, page_view,
    category_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('post/<slug:slug>/', post_detail, name='detail'),
    path('cat/<slug:category_slug>/', category_show, name='category_show'),
    path('contact/', contact_view, name='contact'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('search/', search_results, name='search'),
    path('page/', page_view, name='page'),
    path('category/', category_view, name='category'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)