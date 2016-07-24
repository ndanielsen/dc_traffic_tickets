from rest_framework import viewsets
from rest_framework import ISO_8601
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework_gis.filters import DistanceToPointFilter
# from rest_framework_gis.filters import TMSTileFilter
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets

from api import serializers
from api.models import ParkingViolation
from api.filters import IsoDateTimeField
import django_filters

class ParkingFilter(filters.FilterSet):
    # start_ticket_issue_datetime = IsoDateTimeField(name='ticket_issue_datetime', lookup_expr='gte', input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')
    class Meta:
        model = ParkingViolation
        fields = ['rp_plate_state', 'violation_code', 'holiday', 'body_style']

class ParkingViolationSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint in read only
    """
    queryset = ParkingViolation.objects.all()
    serializer_class = serializers.ParkingViolationSerializer
    filter_backends = (DistanceToPointFilter, filters.DjangoFilterBackend,)
    filter_class = ParkingFilter
    bbox_filter_include_overlapping = True # Optional


# class ParkingViolationDateTimeSet(django_filters.FilterSet):
    # max_date = IsoDateTimeField(source='ticket_issue_datetime', lookup_expr='lt', input_formats=(ISO_8601, '%m/%d/%Y %H:%M:%S'))

    class Meta:
        model = ParkingViolation
        # fields = ['ticket_issue_datetime' ]
