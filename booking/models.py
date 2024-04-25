from django.db import models
from base.models import BaseModel
import uuid

# Create your models here.

class Venue(BaseModel):
    name = models.CharField(max_length=100)
    AC = models.BooleanField()

    def __str__(self)-> str:
        return self.name
    

class Levels(BaseModel):
    level = models.CharField(max_length=100)

    def __str__(self)-> str:
        return self.level
    

class Media_sel(BaseModel):
    media_type = models.CharField(max_length=100)

    def __str__(self)-> str:
        return self.media_type
    

class Slots(BaseModel):
    slot = models.CharField(max_length=2)
    time_period = models.CharField(max_length=15)

    def __str__(self)-> str:
        return self.slot


class Booking_request(BaseModel):
    booking_number = models.CharField(max_length=10, unique=True, default=uuid.uuid4, editable=False)
    program_title = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(null=True)
    requested_dep = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue,blank=True,on_delete=models.CASCADE)
    ac = models.BooleanField(default=False)
    slots = models.ManyToManyField(Slots,blank=True)
    coordinator = models.CharField(max_length=200,blank=True)
    contact_no = models.CharField(max_length=10,blank=True)
    participants = models.PositiveIntegerField(blank=True)
    level = models.ForeignKey(Levels,on_delete=models.CASCADE)
    sponsor = models.CharField(max_length=100,blank=True)
    chief_guest = models.CharField(max_length=100,blank=True)
    program_obj = models.TextField(max_length=100,blank=True)
    media = models.ForeignKey(Media_sel,on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    is_queue = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_postpone = models.BooleanField(default=False)

    
    def __str__(self)-> str:
        return f"{self.program_title}"
    


class Booking_approval(BaseModel):
    AC_CHOICES = (
        ('free','free'),
        ('paid','paid'),
    )
    booking_id = models.ForeignKey(Booking_request,on_delete=models.CASCADE)
    princi_app = models.CharField(default='pending',max_length=20)
    admin_app = models.CharField(default='pending',max_length=20)
    ac_paid = models.CharField(choices=AC_CHOICES, max_length=20,blank=True)
    reason_princi = models.TextField(blank=True)
    reason_admin = models.TextField(blank=True)
    status = models.CharField(default='pending',max_length=20) 
    is_postpone = models.BooleanField(default=False)

    def __str__(self)-> str:
        return f"{self.booking_id}"



class Booking_postpone(BaseModel):
    booking_id = models.ForeignKey(Booking_request,on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slots,blank=True)
    date = models.DateField(null=True)
    
    def __str__(self)-> str:
        return f"{self.booking_id}"


class media_req(BaseModel):
    booking_id = models.ForeignKey(Booking_request,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    reason = models.TextField()


    def __str__(self)-> str:
        return f"{self.booking_id}"

