from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(event)
admin.site.register(Product)
admin.site.register(food)
admin.site.register(Address)
admin.site.register(Booking)
admin.site.register(BookingFood)

