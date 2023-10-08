from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Booking_request)
admin.site.register(Venue)
admin.site.register(Slots)
admin.site.register(Media)
admin.site.register(Levels)

