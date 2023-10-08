from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Venue, Booking_request, Slots, Levels, Media
from datetime import date
from django.http import HttpResponse

# Create your views here.

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user is not None: 
            if user.is_staff:
                login(request, user)
                if user.username == 'bookingAdmin':
                    return redirect('bookingHome')  # Redirect to the user's profile or any desired page
                elif user.username == 'mediaAdmin':
                    return redirect('mediaHome')
                else:
                    return HttpResponse("You have no access ")
            else:
                return HttpResponse("You are not a staff member")

    return render(request, 'booking-admin/login.html')



def is_media_admin(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='mediaAdmin').exists():
            return True
        else:
            return HttpResponse('you are not a media admin')
    else:
        return HttpResponse('you are logged out')



def is_booking_admin(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='bookingAdmin').exists():
            return True
        else:
            return HttpResponse('you are not a media admin')
    else:
        return HttpResponse('you are logged out')

def delete_expired():
    today = date.today()
    obj = Booking_request.objects.filter(date__lt=today)
    obj.delete()
    return


@login_required
def adminLogout(request):
    logout(request)
    return redirect('loginPage')



@login_required
def bookingHome(request):
    if is_booking_admin(request):
        delete_expired()
        bookings = Booking_request.objects.filter(status='Pending').order_by('-created_at')
        context = {'bookings':bookings}
        return render(request, 'booking-admin/booking-home.html',context)
    
@login_required
def approveBooking(request, pk):
    if is_booking_admin(request):
        obj = Booking_request.objects.get(id=pk)
        obj.status = 'Success'
        obj.save()
        return redirect('bookingHome')
    
@login_required
def rejectBooking(request, pk):
    if is_booking_admin(request):
        obj = Booking_request.objects.get(id=pk)
        obj.status = 'Rejected'
        obj.save()
        return redirect('bookingHome')
    

    
def approvedBookingList(request):
    if is_booking_admin(request):
        bookings = Booking_request.objects.filter(status='Success').order_by('-created_at')
        context = {'bookings':bookings}
        return render(request, 'booking-admin/approved-list.html',context)
    
    
def rejectedBookingList(request):
    if is_booking_admin(request):
        bookings = Booking_request.objects.filter(status='Rejected').order_by('-created_at')
        context = {'bookings':bookings}
        return render(request, 'booking-admin/rejected-list.html',context)
    


@login_required
def mediaHome(request):
    if is_media_admin(request):
        return render(request, 'booking-admin/home.html')
    
@login_required
def viewRequestForm(request, pk):
    if is_booking_admin(request):
        booking = Booking_request.objects.get(id=pk)
        context = {'booking':booking}
        return render(request, 'booking-admin/view-request.html', context)        
