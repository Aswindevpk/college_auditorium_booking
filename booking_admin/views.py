from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Venue, Booking_request, Slots, Booking_approval,media_req
import datetime
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user is not None: 
            if user.is_staff:
                login(request, user)
                if user.username == 'sjcadmin' or user.username == 'sjcmain':
                    return redirect('bookingHome')  # Redirect to the user's profile or any desired page
                elif user.username == 'sjcmedia':
                    return redirect('mediaHome')
                else:
                    return HttpResponse("You have no access ")
            else:
                return HttpResponse("You are not a staff member")

    return render(request, 'booking-admin/login.html')


# def delete_expired():
#     today = date.today()
#     obj = Booking_request.objects.filter(date__lt=today)
#     obj.delete()
#     return


@login_required
def adminLogout(request):
    logout(request)
    return redirect('adminLogin')


@login_required
def bookingHome(request):
    bookings = []
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    if request.user.username == 'sjcmain':
        try:
            # fetch only request of bookings that is not expired 
            bookings_ids = Booking_approval.objects.filter(admin_app ='success',princi_app='pending').values_list('booking_id')
            bookings = Booking_request.objects.filter(id__in=bookings_ids,date__gt=current_date)
        except:
            print('error')
    elif request.user.username == 'sjcadmin':
        try:
            # fetch only request of bookings that is not expired 
            bookings_ids = Booking_approval.objects.filter(admin_app = 'pending').values_list('booking_id')
            bookings = Booking_request.objects.filter(id__in=bookings_ids,date__gt=current_date)
        except:
            print('error')
    context = {'bookings':bookings}
    return render(request, 'booking-admin/booking-home.html',context)

    
@login_required
def approveBooking(request, pk):
    obj = Booking_approval.objects.get(booking_id=pk)
    if request.user.username == 'sjcmain':
        obj.princi_app = 'success'
    elif request.user.username == 'sjcadmin':
        obj.admin_app = 'success'

    #make it success only if both of that is success
    if obj.princi_app == 'success' and obj.admin_app == 'success':
        obj.status = 'success'

        #make the booking request object is approved success
        booking_obj = Booking_request.objects.get(id=pk)
        booking_obj.is_approved = True
        booking_obj.save()

    obj.save()
    return redirect('bookingHome')
    

@login_required
@require_POST
def rejectBooking(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        pk = request.POST.get('id')
        obj = Booking_approval.objects.get(booking_id=pk)

        if request.user.username == 'sjcmain':
            obj.princi_app = 'reject'
            obj.reason_princi = reason
        elif request.user.username == 'sjcadmin':
            obj.admin_app = 'reject'
            obj.reason_admin = reason

        if obj.princi_app or obj.admin_app == 'reject':
            obj.status = 'reject'
        
            booking_obj = Booking_request.objects.get(id=obj.booking_id.id)
            booking_obj.is_rejected = True
            booking_obj.save()

        obj.save()
    return redirect('bookingHome')
    

@login_required
def approvedBookingList(request):

    if request.user.username == 'sjcmain':
        bookings_ids = Booking_approval.objects.filter(princi_app='success',status='success').values_list('booking_id')
    elif request.user.username == 'sjcadmin':
        bookings_ids = Booking_approval.objects.filter(admin_app='success').values_list('booking_id')

    bookings = Booking_request.objects.filter(id__in=bookings_ids).order_by('-created_at')
    context = {'bookings':bookings}
    return render(request, 'booking-admin/approved-list.html',context)
    
@login_required
def rejectedBookingList(request):

    if request.user.username == 'sjcmain':
        bookings_ids = Booking_approval.objects.filter(princi_app='reject',status='reject').values_list('booking_id')
    elif request.user.username == 'sjcadmin':
        bookings_ids = Booking_approval.objects.filter(admin_app='reject').values_list('booking_id')

    bookings = Booking_request.objects.filter(id__in=bookings_ids).order_by('-created_at')
    context = {'bookings':bookings}
    return render(request, 'booking-admin/rejected-list.html',context)
    
    
@login_required
def viewRequestForm(request, pk):
    booking = Booking_request.objects.get(id=pk)
    context = {'booking':booking}
    return render(request, 'booking-admin/view-request.html', context)  


    
@login_required
def viewRequestFormApproved(request, pk):
    booking = Booking_request.objects.get(id=pk)
    context = {'booking':booking}
    return render(request, 'booking-admin/view-request-approved.html', context) 


@login_required
def viewRequestFormRejected(request, pk):
    booking = Booking_request.objects.get(id=pk)
    context = {'booking':booking}
    return render(request, 'booking-admin/view-request-rejected.html', context) 






@login_required
def mediaHome(request):
    medias = media_req.objects.all()
    context = {'medias':medias}
    return render(request, 'booking-admin/media-home.html',context)
