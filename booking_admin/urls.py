from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminLogin,name='adminLogin'),
    path('media/',views.mediaHome,name='mediaHome'),
    path('booking/',views.bookingHome,name='bookingHome'),
    path('approve-booking/<str:pk>',views.approveBooking,name='approveBooking'),
    path('reject-booking/<str:pk>',views.rejectBooking,name='rejectBooking'),
    path('approved-booking-list/',views.approvedBookingList,name='approvedBookingList'),
    path('rejected-booking-list/',views.rejectedBookingList,name='rejectedBookingList'),
    path('logout/',views.adminLogout,name='adminLogout'),
    path('view-request-form/<str:pk>',views.viewRequestForm,name='viewRequestForm'),

]