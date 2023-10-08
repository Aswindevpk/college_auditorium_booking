from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

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
    



class Media(BaseModel):
    media = models.CharField(max_length=50)

    def __str__(self)-> str:
        return self.media
    



class Slots(BaseModel):
    slot = models.CharField(max_length=2)
    time_period = models.CharField(max_length=15)

    def __str__(self)-> str:
        return self.slot


class Booking_request(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Rejected', 'Rejected'),
    )
    LEVELS = (
        ('National', 'National'),
        ('State', 'State'),
        ('College', 'College'),
    )
    MEDIA_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('both', 'Both Photo and Video'),
        ('none', 'No Media'),
    )

    program_title = models.CharField(max_length=200,null=True,blank=True)
    date = models.DateField(null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    requested_dep = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue,blank=True,on_delete=models.CASCADE)
    ac = models.BooleanField(default=False)
    time_slots = models.ManyToManyField(Slots,blank=True)
    coordinator = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=10)
    expected_no_of_participants = models.PositiveIntegerField()
    level = models.ForeignKey(Levels,blank=True,on_delete=models.CASCADE)
    sponsor = models.CharField(max_length=100)
    chief_guest = models.CharField(max_length=100)
    objective_of_programme = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    media_selection = models.ForeignKey(Media,blank=True,on_delete=models.CASCADE)
    reason = models.TextField(blank=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.program_title)
        super(Booking_request,self).save(*args, **kwargs)
    
    def __str__(self)-> str:
        return f"{self.program_title} status :{self.status}"
    




