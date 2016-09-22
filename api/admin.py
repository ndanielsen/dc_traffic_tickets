from django.contrib.gis import admin
from rest_framework.authtoken.admin import TokenAdmin
from leaflet.admin import LeafletGeoAdmin


# Register your models here.
from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles

@admin.register(ParkingViolation)
class ParkingViolationAdmin(LeafletGeoAdmin):
    # openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.18.2/ol.js'
    modifiable = False
    list_display = ('violation_code', 'ticket_issue_datetime')
    readonly_fields =  ('ticket_issue_datetime','address_id', 'address', 'rp_plate_state', 'violation_code',  'body_style', 'holiday', 'streetsegid', 'xcoord', 'ycoord', 'filename', 'rowid', 'objectid', 'violation_description' )
    settings_overrides = {
       'DEFAULT_ZOOM': 14,
       'NO_GLOBALS' : False,
    }




@admin.register(ParkingViolationDataFiles)
class ParkingViolationDataFilesAdmin(admin.GeoModelAdmin):
    list_display = ('filename', 'imported', 'date_added' )
    readonly_fields = ('imported',)
