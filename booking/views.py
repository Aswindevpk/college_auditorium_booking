from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Venue, Booking_request, Slots, Levels, Media
import datetime
from django.http import HttpResponse


def is_normal_user(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return True
    else:
        logout(request)
        return HttpResponse('your are a staff')
        

@login_required
def home(request):
    if is_normal_user(request):
        user = request.user
        if request.method == 'POST':
            #date if user give the date
            search_date = request.POST.get('date')
        else:
            #if user does not give the date use current date
            search_date = datetime.date.today().strftime("%Y-%m-%d")
        
        venues = Venue.objects.all()
        slots_list = Slots.objects.all()
        bookings = Booking_request.objects.filter(date=search_date)

        available_venues = []

        for venue in venues:
            venue_avail = {'venue':venue, 'slots':{},'all_booked':False}

            slots_avail = []
            for slots in slots_list:
                temp = {'status':'free','time_period':slots.time_period}
                slots_avail.append(temp)
                

            for booking in bookings:
                if booking.venue == venue:
                    slots = booking.time_slots.all()
                    if booking.status == 'Pending':
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='Pending'
                    elif booking.status == 'Success':
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='Success'
                    elif booking.status == 'Rejected':
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='free'

            venue_avail['slots'] = slots_avail

            # if no more free slot diable the book button by all_booked to True 
            for item in slots_avail:
                if item['status'] == 'free':
                    venue_avail['all_booked'] = False
                    break
                else:
                    venue_avail['all_booked'] = True



            available_venues.append(venue_avail)
        
        context = {'user':user , 'search_date':search_date, 'available_venues': available_venues }

        return render(request, 'home.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required
def bookingCancel(request, pk):
    if is_normal_user(request):
        booking = Booking_request.objects.get(id=pk)
        booking.delete()
        return redirect('bookingHistory')


@login_required
def bookingHistory(request):
    if is_normal_user(request):
        user = request.user
        bookings = Booking_request.objects.filter(requested_dep=user).order_by('-created_at')

        context = {'bookings':bookings}
        return render(request, 'booking_history.html',context)



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user is not None:
            if not user.is_staff:
                login(request, user)
                return redirect('home')  # Redirect to the user's profile or any desired page
            else:
                return HttpResponse("You are a staff member.")

    return render(request, 'login.html')



@login_required
def booking_form(request, venue, search_date):
    date = search_date
    venue = Venue.objects.get(name=venue)
    user = request.user
    levels = Levels.objects.all()
    medias = Media.objects.all()

    # finding free slots 
    slots = Slots.objects.all()
    bookings = Booking_request.objects.filter(date=date, venue=venue)

    slots_avail = []
    for slot in slots:
        temp = {'status':'free','time_period':slot.time_period, 'id':slot.id}
        slots_avail.append(temp)
            

    for booking in bookings:
        if booking.venue == venue:
            slots = booking.time_slots.all()
            if booking.status == 'Pending':
                for slot in slots:
                    slots_avail[int(slot.slot)]['status']='Pending'
            elif booking.status == 'Success':
                for slot in slots:
                    slots_avail[int(slot.slot)]['status']='Success'
            elif booking.status == 'Rejected':
                for slot in slots:
                    slots_avail[int(slot.slot)]['status']='free'

    print(venue.AC)
    context ={'date':date, 'venue':venue, 'user':user, 'levels':levels, 'medias':medias, 'slots_avail':slots_avail}
    return render(request, 'booking_form.html',context )    

@login_required
def bookingRequest(request):
    if request.method == 'POST':
        program_title = request.POST.get('program_title')
        date = request.POST.get('date')
        requested_dep = request.POST.get('requested_dep')
        venue = Venue.objects.get(id=request.POST.get('venue'))
        ac = request.POST.get('ac')
        time_slots = Slots.objects.filter(id__in=request.POST.getlist('time_slots'))
        coordinator = request.POST.get('coordinator')
        contact_no = request.POST.get('contact_no')
        expected_no_of_participants = request.POST.get('expected_no_of_participants')
        level = Levels.objects.get(id=request.POST.get('level'))
        sponsor = request.POST.get('sponsor')
        chief_guest = request.POST.get('chief_guest')
        objective_of_programme = request.POST.get('objective_of_programme')
        status = 'Pending'
        media_selection = Media.objects.get(id=request.POST.get('media_selection'))

        if ac == 'ac':
            ac = True
        else:
            ac = False

        
        booking_instance = Booking_request(program_title=program_title, date= date, requested_dep= requested_dep,venue=venue, ac=ac,
                                            coordinator= coordinator, contact_no=contact_no, expected_no_of_participants=expected_no_of_participants,
                                           level=level,sponsor=sponsor,chief_guest=chief_guest, objective_of_programme =objective_of_programme,
                                           status=status, media_selection= media_selection)
        booking_instance.save()
        booking_instance.time_slots.set(time_slots)
        
        
    return render(request, 'booking_success.html' ) 


@login_required
def viewForm(request, pk):
    if is_normal_user(request):
        booking = Booking_request.objects.get(id=pk)

        context = {'booking':booking}
        return render(request, 'view-form.html', context)









