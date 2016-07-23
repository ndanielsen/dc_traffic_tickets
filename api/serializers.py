from rest_framework import serializers

from api.models import ParkingViolation

class ParkingViolationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingViolation
        fields = '__all__'
