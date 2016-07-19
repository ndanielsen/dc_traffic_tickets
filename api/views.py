from rest_framework import viewsets
from api.serializers import ParkingViolationSerializer
from api.models import ParkingViolation

class ParkingViolationSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ParkingViolation.objects.all()
    serializer_class = ParkingViolationSerializer
