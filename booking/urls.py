from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage, name='loginPage'),
    path('logout/',views.logoutUser, name='logoutUser'),
    path('booking-history/',views.bookingHistory, name='bookingHistory'),
    path('booking_form/<str:venue>/<str:search_date>',views.booking_form, name='booking_form'),
    path('booking-request/',views.bookingRequest, name='booking-request'),
    path('booking-cancel/<str:pk>',views.bookingCancel, name='booking-cancel'),
    path('view-form/<str:pk>',views.viewForm,name='viewForm'),
]