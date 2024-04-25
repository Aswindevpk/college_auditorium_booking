from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage, name='loginPage'),
    path('logout/',views.logoutUser, name='logoutUser'),
    path('booking-history/',views.bookingHistory, name='bookingHistory'),
    path('booking-rejected/',views.bookingRejected, name='bookingRejected'),
    path('reject-reason/<str:pk>',views.rejectReason,name='rejectReason'),
    path('booking_form/<str:venue>/<str:search_date>',views.booking_form, name='booking_form'),
    path('booking-request/',views.bookingRequest, name='booking-request'),
    path('booking-postpone/<str:pk>',views.bookingPostpone, name='booking-postpone'),
    path('booking-cancel/<str:pk>',views.bookingCancel, name='booking-cancel'),
    path('check-available/',views.checkAvailable, name='check-available'),
    path('view-form/<str:pk>',views.viewForm,name='viewForm'),
    path('postpone-request-preview/',views.PostponeRequestPreview,name='postpone-request-preview'),
    path('postpone-request-submit/',views.PostponeRequestSubmit,name='postpone-request-submit'),
]