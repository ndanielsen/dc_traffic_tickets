from rest_framework import viewsets
from rest_framework import ISO_8601
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets

from api import serializers
from api.models import ParkingViolation
from api.filters import IsoDateTimeField
import django_filters

class ParkingViolationSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint in read only
    """
    queryset = ParkingViolation.objects.all()
    serializer_class = serializers.ParkingViolationSerializer
    # filter_backends = (filters.DjangoFilterBackend,)


# class User(django_filters.FilterSet):
#     # ticket_issue_datetime = IsoDateTimeField(lookup_expr='iexact', input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
#     # max_date = IsoDateTimeField(source='ticket_issue_datetime', lookup_expr='lt', input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))
#
#     class Meta:
#         model = ParkingViolation
#         fields = ['ticket_issue_datetime' ]
