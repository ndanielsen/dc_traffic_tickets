from django.contrib import admin

# Register your models here.
from api.models import ParkingViolation

@admin.register(ParkingViolation)
class ParkingViolationAdmin(admin.ModelAdmin):
    pass
