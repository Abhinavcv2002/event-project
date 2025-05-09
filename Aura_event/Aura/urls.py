from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('about',views.about,name="about"),
    path('signout',views.signout,name='signout'),
    path('weding',views.weding,name='weding'),
    path('contact',views.contact,name='contact'),
    path('gallery',views.gallery,name='gallery'),
    path('wed_details',views.wed_details,name='wed_details'),
    path('cop_event',views.cop_event,name='cop_event'),
    path('cop_details',views.cop_details,name='cop_details'),
    path('birthday',views.birthday,name='birthday'),
    path('birthday_details',views.birthday_details,name='birthday_details'),

    path('admin_page',views.admin_page,name='admin_page'),
]
