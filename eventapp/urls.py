from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user_register', views.user_register, name='user_register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('vendors', views.vendors, name='vendors'),
    path('contact', views.contact, name='contact'),
    path('vendor_register', views.vendor_register, name='vendor_register'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('admin_user_view', views.admin_user_view, name='admin_user_view'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('vendor_index', views.vendor_index, name='vendor_index'),
    path('admin_vendor_view/', views.admin_vendor_view, name='admin_vendor_view'),
    path('approve_vendor/<int:id>/', views.approve_vendor, name='approve_vendor'),
    path('reject_vendor/<int:id>/', views.reject_vendor, name='reject_vendor'),
    path('service_add/', views.service_add, name='service_add'),
]
