from django.contrib import admin
from .models import PasswordReset
from .models import Reservation
from .models import Profile

admin.site.register(PasswordReset)
# Register your models here.


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'contact_number', 'pickup_date', 'dropoff_date', 'vehicle', 'created_at')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'contact_number', 'address']
    list_filter = ['role']
