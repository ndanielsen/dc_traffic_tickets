from rest_framework import serializers

from api.models import ParkingViolation

class ParkingViolationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingViolation
        fields = ('location', 'ticket_issue_datetime', 'address', 'violation_code')
