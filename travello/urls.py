from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('search', views.search, name='search'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_list/destination_details/pessanger_detail_def/<str:city_name>',views.pessanger_detail_def,name='pessanger_detail_def'),
    path('upcoming_trips', views.upcoming_trips, name='upcoming_trips'),
    path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/card_payment', views.card_payment, name='card_payment'),
    path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/otp_verification', views.otp_verification, name='otp_verification'),
    path('destination_list/destination_details/pessanger_detail_def/pessanger_detail_def/net_payment', views.net_payment, name='net_payment'),
    path('new_page',views.new_page_view,name='new_page'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin', views.login, name='admin'),
    path('admin_bookings', views.adminbooking, name='adminbooking'),
    path('delete_booking/<int:trip_id>/', views.delete_booking, name='delete_booking'),
    path('admin_viewusers/', views.adminviewuser, name='admin_viewusers'),
    path('users/', views.adminviewuser, name='users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_destination/', views.admin_destination, name='admin_destination'),
    path('delete_country/<int:country_id>/', views.delete_country, name='delete_country'),
    path('delete_detailed_desc/<int:detailed_desc_id>/', views.delete_detailed_desc, name='delete_detailed_desc'),
    path('edit_country/<int:destination_id>/', views.edit_country, name='edit_country'),
    path('edit_detailed_desc/<int:detailed_desc_id>/', views.edit_places, name='edit_detailed_desc'),
    

]
