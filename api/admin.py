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
    date_hierarchy = "ticket_issue_datetime"
    list_display = ('ticket_issue_datetime', "violation_code")
    readonly_fields =  ('address', 'ticket_issue_datetime','address_id', 'rp_plate_state', 'violation_code',  'body_style', 'holiday', 'streetsegid', 'xcoord', 'ycoord', 'data_filename', 'rowid', 'objectid', 'violation_description' )
    settings_overrides = {
        'DEFAULT_ZOOM': 13,
        'MIN_ZOOM': 10,
        'MAX_ZOOM': 13,
    }

@admin.register(ParkingViolationDataFiles)
class ParkingViolationDataFilesAdmin(admin.GeoModelAdmin):
    list_display = ('filename', 'imported', 'date_added' )
    readonly_fields = ('imported',)

@admin.register(ParkingViolationFine)
class ParkingViolationFineAdmin(admin.GeoModelAdmin):
    list_display = ('violation_code', 'description', 'fine')
    readonly_fields = ('violation_code', 'description', 'fine', 'short_description', 'json_data')
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AddressID)
class AddressIDAdmin(LeafletGeoAdmin):
    modifiable = False
    list_display = ('address_id', 'ward', 'quadrant', 'zipcode', 'official_status', 'residential_type')
    readonly_fields = ('address_id', 'ward', 'quadrant', 'zipcode', 'official_status', 'residential_type', 'police_service_area', 'police_district', 'address_suffix', 'street_name', 'street_type', 'address_num', 'census_block', 'census_blockgroup', 'census_tract', 'resident_occupancy_count', 'advisory_neighborhood_commission', 'single_member_district', 'vote_precinct', 'json_data', 'neighbor_hood', 'neighbor_hood_cluster')
    settings_overrides = {
        'DEFAULT_ZOOM': 13,
        'MIN_ZOOM': 13,
        'MAX_ZOOM': 15,
    }


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
