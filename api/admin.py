from django.contrib.gis import admin
from rest_framework.authtoken.admin import TokenAdmin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles

@admin.register(ParkingViolation)
class ParkingViolationAdmin(admin.OSMGeoAdmin):
    date_hierarchy = 'ticket_issue_datetime'
    list_display = ('rowid', 'violation_code', 'filename', 'ticket_issue_datetime')


@admin.register(ParkingViolationDataFiles)
class ParkingViolationDataFilesAdmin(admin.GeoModelAdmin):
    readonly_fields = ('imported',)
    pass
