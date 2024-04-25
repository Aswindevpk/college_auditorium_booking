from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Booking_request)
admin.site.register(Venue)
admin.site.register(Slots)
admin.site.register(Booking_approval)
admin.site.register(Booking_postpone)
admin.site.register(media_req)
admin.site.register(Levels)
admin.site.register(Media_sel)

