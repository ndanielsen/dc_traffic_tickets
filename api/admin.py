from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
from api.models import ParkingViolation

@admin.register(ParkingViolation)
class ParkingViolationAdmin(admin.ModelAdmin):
    pass
