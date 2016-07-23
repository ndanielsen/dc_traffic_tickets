from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination

from api.serializers import ParkingViolationSerializer
from api.models import ParkingViolation

class ParkingViolationSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ParkingViolation.objects.all()
    serializer_class = ParkingViolationSerializer
    # pagination_class = GeoJsonPagination
