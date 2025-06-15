from django.contrib import admin
from .models import Ride,Booking,User
# Register your models here.
admin.site.register(User)
admin.site.register(Ride)
admin.site.register(Booking)
