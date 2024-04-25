from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Venue, Booking_request, Slots, Booking_approval,Levels,Media_sel,media_req
import datetime
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def is_normal_user(request):
    #if authenticated and not a staff member
    if request.user.is_authenticated and not request.user.is_staff:
        return True
    
    #else show you are a staff
    else:
        logoutUser(request)
        return HttpResponse('your are a staff')
        

@login_required
def home(request):
    if is_normal_user(request):
        user = request.user
        if request.method == 'POST':
            #date if user give the date
            search_date = request.POST.get('date')
        else:
            #if user does not give the date use next available date
            current_date = datetime.date.today()
            # Calculate the date for the next day
            next_day = current_date + datetime.timedelta(days=1)

            # Format the date as a string
            search_date = next_day.strftime("%Y-%m-%d")
        
        venues = Venue.objects.all()
        slots_list = Slots.objects.all()
        bookings = Booking_request.objects.filter(date=search_date,is_cancelled=False)

        available_venues = []

        for venue in venues:
            venue_avail = {'venue':venue, 'slots':{},'all_booked':False}

            slots_avail = []
            for slots in slots_list:
                temp = {'status':'free','time_period':slots.time_period}
                slots_avail.append(temp)
                

            for booking in bookings:
                if booking.venue == venue:
                    slots = booking.slots.all()
                    if booking.is_approved:
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='Success'
                    elif booking.is_cancelled or booking.is_rejected:
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='free'
                    else:
                        for slot in slots:
                            slots_avail[int(slot.slot)]['status']='Pending'


            venue_avail['slots'] = slots_avail

            # if no more free slot disable the book button by all_booked to True 
            venue_avail['all_booked'] = True
            for item in slots_avail:
                if item['status'] != 'Success':
                    venue_avail['all_booked'] = False


            available_venues.append(venue_avail)

        context = {'user':user , 'search_date':search_date, 'available_venues': available_venues}

        return render(request, 'home.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('loginPage')


# check if any available slot in the specified date 
def checkAvailable(request):
    if is_normal_user(request):
        if request.method == 'POST':
            search_date = request.POST.get('date')
            venue_sel =Venue.objects.get(id=request.POST.get('venue'))
            pk = request.POST.get('pk')
            booking = Booking_request.objects.get(id=pk)

    
            bookings = Booking_request.objects.filter(is_rejected=False,date=search_date,venue=venue_sel)
            venues = Venue.objects.all()
            
            # set both as free slots 
            slots_list = Slots.objects.all()

            # if  bookings exists 
            if bookings.count() != 0:
                for book in bookings:
                    slots_to_exclude = book.slots.all().values_list('pk', flat=True)
                    slots_list = slots_list.exclude(pk__in=slots_to_exclude)
            
                
            context = {'booking':booking,'venues':venues,'venue_sel':venue_sel,'search_date':search_date,'slots_list':slots_list}
            return render(request,'postpone-form.html',context)




@login_required
def bookingPostpone(request, pk):
    if is_normal_user(request):
        booking = Booking_request.objects.get(id=pk)
        venue = booking.venue
        current_date = datetime.date.today()
        # Calculate the date for the next day
        next_day = current_date + datetime.timedelta(days=1)

        # Format the date as a string
        search_date = next_day.strftime("%Y-%m-%d")

        venues = Venue.objects.all()


        context = {'booking':booking,'venue':venue,'search_date':search_date, 'venues':venues}
        return render(request,'postpone-form.html',context)

@login_required
def PostponeRequestPreview(request):
    if is_normal_user(request):
        if request.method == 'POST':
            date = request.POST.get('date')
            venue = Venue.objects.get(id=request.POST.get('venue'))
            pk = request.POST.get('pk')
            slots = Slots.objects.filter(id__in=request.POST.getlist('time_slots'))



            booking = Booking_request.objects.get(id=pk)
            booking.date = date
            booking.venue = venue
            booking.slots.set(slots)


            context = {'booking':booking}
            return render(request, 'postpone-preview.html',context)
        

@login_required
def PostponeRequestSubmit(request):
    if is_normal_user(request):
        if request.method == 'POST':
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Access individual fields from the JSON data
            pk = data.get('pk')
            date = data.get('date')
            venue = Venue.objects.get(id=data.get('venue'))
            slots = Slots.objects.filter(id__in=data.get('slots'))

            booking = Booking_request.objects.get(id=pk)
            booking.date = date
            booking.venue = venue
            booking.slots.set(slots)
            booking.is_approved = False
            booking.is_postpone = True
            booking.save()

            #approved list instance
            instance_to_delete = Booking_approval.objects.get(booking_id=booking.id)
            # delete old instance 
            instance_to_delete.delete()

            #new instance
            Booking_approval.objects.create(booking_id=booking,is_postpone=True)


            response_data = {'success': True, 'message': 'Booking confirmed successfully'}
            return JsonResponse(response_data)
    



@login_required
def bookingCancel(request, pk):
    if is_normal_user(request):
            def alreadyBooked(date, venue):
                #function returns the slot of bookings that is not in queue   
                #empty slot variable
                slot = Slots.objects.none()
                #give the list of requests that is not in queue
                bookings = Booking_request.objects.filter(date=date,is_queue=False,venue=venue)

                for booking in bookings:
                    # Adds the slots associated with each booking to the slot queryset. The | operator performs a union of querysets.
                    slot = slot | booking.slots.all()
                return slot

            booking = Booking_request.objects.get(id=pk)
            date = booking.date
            venue = booking.venue

        
            # delete the instance in the booking approval in cancellation of the pending request that is gone to admin
            if booking.is_queue == False:
                # delete that perticular request that is sent to admin 
                instance_to_delete = Booking_approval.objects.get(booking_id=booking.id)
                # delete that instance 
                instance_to_delete.delete()

                #delete the booking instance also
                booking.delete()

                # give the list of bookings that is in queue 
                queue_bookings = Booking_request.objects.filter(venue=venue,date=date,is_queue=True).order_by('created_at')
                # iterate queue bookings 
                for queue_book in queue_bookings:
                    a_slot = alreadyBooked(date=date,venue=venue) #already booked slots returned by alreadybooked function

                    vacency = True        #initailly set as true

                    for slot in queue_book.slots.all():

                        if slot in a_slot:
                            vacency = False   #no slot available

                    if vacency:
                        #if slots are available set queue as false
                        queue_book.is_queue = False
                        queue_book.save()
                        #create and instance for admin approval because it is in not queue
                        Booking_approval.objects.create(booking_id=queue_book)
                        # add to media req when it is not in queue 
                        if str(queue_book.media) != "None":
                            media_req.objects.create(booking_id=queue_book)
                    
            else:
                booking.delete()

            return redirect('bookingHistory')



@login_required
def bookingHistory(request):
    if is_normal_user(request):
        user = request.user
        bookings = Booking_request.objects.filter(requested_dep=user,is_cancelled=False,is_rejected=False).order_by('-created_at')

        context = {'bookings':bookings,'heading':'Pending Booking History'}
        return render(request, 'booking_history.html',context)
    

    
@login_required
def bookingRejected(request):
    if is_normal_user(request):
        user = request.user
        bookings = Booking_request.objects.filter(requested_dep=user,is_rejected=True).order_by('-created_at')
        context = {'bookings':bookings,'heading':'Rejected Booking History'}
        return render(request, 'booking_rejected.html',context)
    

@login_required
def rejectReason(request,pk):
    if is_normal_user(request):
        reject_reason = Booking_approval.objects.get(booking_id=pk)
        context = {'reason':reject_reason}
        return render(request, 'reject_reason.html',context)



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
    media_sel = Media_sel.objects.all()

    # finding free slots 
    slots = Slots.objects.all()
    bookings = Booking_request.objects.filter(date=date, venue=venue)

    slots_avail = []
    for slot in slots:
        temp = {'status':'free','time_period':slot.time_period, 'id':slot.id}
        slots_avail.append(temp)
            

    for booking in bookings:
        if booking.venue == venue:
            slots = booking.slots.all()
            if booking.is_approved:
                for slot in slots:
                    slots_avail[int(slot.slot)]['status']='Success'
            else:
                for slot in slots:
                    slots_avail[int(slot.slot)]['status']='free'

    context ={'date':date, 'venue':venue, 'user':user, 'slots_avail':slots_avail, 'medias':media_sel,'levels':levels}
    return render(request, 'booking_form.html',context )    


@login_required
def bookingRequest(request):
    if request.method == 'POST':
        program_title = request.POST.get('program_title')
        date = request.POST.get('date')
        requested_dep = request.POST.get('requested_dep')
        venue = Venue.objects.get(id=request.POST.get('venue'))
        ac = request.POST.get('ac')
        slots = Slots.objects.filter(id__in=request.POST.getlist('time_slots'))
        coordinator = request.POST.get('coordinator')
        contact_no = request.POST.get('contact_no')
        participants = request.POST.get('expected_no_of_participants')
        level = Levels.objects.get(id=request.POST.get('level'))
        sponsor = request.POST.get('sponsor')
        chief_guest = request.POST.get('chief_guest')
        program_obj = request.POST.get('objective_of_programme')
        media = Media_sel.objects.get(id=request.POST.get('media_selection'))


        if ac == 'ac':
            ac = True
        else:
            ac = False


        is_queue = False
        try:
            already_booked = Booking_request.objects.filter(date=date,is_cancelled=False,is_queue=False,is_rejected=False,venue=venue)
            
            #set the queue true if the same slot exist
            if already_booked:
                for booked in already_booked:
                    prev_slots = booked.slots.all()
                    new_slots = slots
                    for slot in new_slots:
                        if slot in prev_slots:
                            is_queue = True

        except Booking_request.DoesNotExist:
            print("The object does not exist.")

        booking_instance = Booking_request(program_title=program_title, date= date, requested_dep= requested_dep,venue=venue, ac=ac,
                                            coordinator= coordinator, contact_no=contact_no, participants=participants,
                                           level=level,sponsor=sponsor,chief_guest=chief_guest, program_obj = program_obj
                                           , media = media,is_queue=is_queue)
        booking_instance.save()
        booking_instance.slots.set(slots)
        booking_number = booking_instance.booking_number

        #if not is queue create approval instance
        if not is_queue:
            Booking_approval.objects.create(booking_id=booking_instance)

            # add to media req when it is not in queue 
            if str(media) != "None":
                media_req.objects.create(booking_id=booking_instance)
                

        context = {'booking_number':booking_number}
    
    return render(request, 'booking_success.html',context ) 


@login_required
def viewForm(request, pk):
    if is_normal_user(request):
        booking = Booking_request.objects.get(id=pk)

        context = {'booking':booking}
        return render(request, 'view-form.html', context)









