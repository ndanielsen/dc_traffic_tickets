from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from api.models import ParkingViolation

class ParkingViolationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ParkingViolation
        geo_field = "point"
        exclude =  ('address_id', 'streetsegid', 'xcoord', 'ycoord', 'data_filename', 'rowid', 'objectid', 'violation_description' )

class GeoParkingViolationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ParkingViolation
        geo_field = "point"
        fields =  ('violation_code', 'ticket_issue_datetime')
        # exclude =  ('address_id', 'address', 'streetsegid', 'xcoord', 'ycoord', 'data_filename', 'rowid', 'objectid', 'violation_description' )
