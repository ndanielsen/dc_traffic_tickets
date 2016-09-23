from django.contrib.gis import admin
from rest_framework.authtoken.admin import TokenAdmin
from leaflet.admin import LeafletGeoAdmin

from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles
from api.models import ParkingViolationFine
from api.models import AddressID
from api.models import StreetSegID
from api.models import BodyStyle
from api.models import PlateState

@admin.register(ParkingViolation)
class ParkingViolationAdmin(LeafletGeoAdmin):
    # openlayers_url = 'https://cdnjs.cloudflare.com/ajax/libs/ol3/3.18.2/ol.js'
    modifiable = False
    list_display = ('ticket_issue_datetime',)
    # readonly_fields =  ('ticket_issue_datetime','address_id', 'address', 'rp_plate_state', 'violation_code',  'body_style', 'holiday', 'streetsegid', 'xcoord', 'ycoord', 'filename', 'rowid', 'objectid', 'violation_description' )
    settings_overrides = {
       'DEFAULT_ZOOM': 14,
       'NO_GLOBALS' : False,
    }

@admin.register(ParkingViolationDataFiles)
class ParkingViolationDataFilesAdmin(admin.GeoModelAdmin):
    list_display = ('filename', 'imported', 'date_added' )
    readonly_fields = ('imported',)

@admin.register(ParkingViolationFine)
class ParkingViolationFineAdmin(admin.GeoModelAdmin):
    list_display = ('code', 'description', 'fine')
    readonly_fields = ('code', 'description', 'fine', 'short_description')
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AddressID)
class AddressIDAdmin(admin.GeoModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

@admin.register(StreetSegID)
class StreetSegIDAdmin(admin.GeoModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

@admin.register(BodyStyle)
class BodyStyleAdmin(admin.GeoModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

@admin.register(PlateState)
class PlateStateAdmin(admin.GeoModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
