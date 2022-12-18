from django.contrib import admin
from django.urls import path, include

from NGMAapp import views

urlpatterns = [
    path("",views.home,name="home"),
    path("Home/",views.home,name="home"),
    path('ContactUs/',views.Contact, name='Contact'),
    path('Checkout/',views.Checkout, name='Checkout'),
    path('AboutUs/',views.About, name='About'),
    path('Employee/',views.Employee, name='Employee'),
    path('Booking/',views.Booking, name='Booking'),
    path('VisitorForm/',views.VisitorForm,name='VisitorForm'),
    path('LoginUser/',views.LoginUser ,name='LoginUser'),
    path('LogoutUser/',views.LogoutUser ,name='LogoutUser'),
    path('Register/',views.Register ,name='Register'),
    path('Artist/',views.Artist ,name='Artist'),
    path('ArtistForm/',views.ArtistForm ,name='ArtistForm'),
    path('Review/',views.Review ,name='Review'),
    path('Checkout/',views.Checkout,name='Checkout'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
    # path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]