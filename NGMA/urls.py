"""NGMA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
# from NGMAapp import urls

admin.site.site_header = "NGMA Admin"
admin.site.site_title = "NGMA Admin Portal"
admin.site.index_title = "Welcome to NGMA Portal"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('NGMAapp.urls')),
    path('Home/',include('NGMAapp.urls')),
    path('VisitorForm/',include('NGMAapp.urls')),
    path('Booking/',include('NGMAapp.urls')),
    path('ContactUs/',include('NGMAapp.urls')),
    path('Checkout/',include('NGMAapp.urls')),
    path('Employee/',include('NGMAapp.urls')),
    path('LoginUser/',include('NGMAapp.urls')),
    path('LogoutUser/',include('NGMAapp.urls')),
    path('Register/',include('NGMAapp.urls')),
    path('Artist/',include('NGMAapp.urls')),
    path('handlerequest/',include('NGMAapp.urls')),
    path('ArtistForm/',include('NGMAapp.urls')),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
