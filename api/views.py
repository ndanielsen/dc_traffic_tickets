from datetime import datetime

from rest_framework import viewsets
from rest_framework import ISO_8601
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework_gis.filters import DistanceToPointFilter
from rest_framework.response import Response
# from rest_framework_gis.filters import TMSTileFilter
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets


from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.utils import dateparse

from api import serializers
from api.models import ParkingViolation
from api.filters import IsoDateTimeField
import django_filters
from django.utils.encoding import force_bytes, force_str, force_text
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


def day_of_week_action(queryset, value):
    # Entry.objects.filter(pub_date__day=3)
    return queryset.filter(
        ticket_issue_datetime__week_day=value,
    )

def oneday_action(queryset, value):
    return queryset.filter(
        ticket_issue_datetime__date=value,
    )

def gt_action(queryset, value):
    return queryset.filter(
        ticket_issue_datetime__gt=value,
    )

def lt_action(queryset, value):
    return queryset.filter(
        ticket_issue_datetime__lt=value,
    )

class ParkingFilter(filters.FilterSet):
    ticket_date_range_start = django_filters.DateTimeFilter(
        name="ticket_issue_datetime",
        action=gt_action,
    )

    ticket_date_range_end = django_filters.DateTimeFilter(
        name="ticket_issue_datetime",
        action=lt_action,
    )
    ticket_single_date = django_filters.DateTimeFilter(
        name="ticket_issue_datetime",
        action=oneday_action,
    )

    ticket_day_of_week = django_filters.NumberFilter(
        name="ticket_issue_datetime",
        action=day_of_week_action,
    )

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

    class Meta:
        model = ParkingViolation

class ApiStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint for heartbeat checking, including the status and version.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def list(self, request):
        return Response({
            "status": "ok",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })

class ParkingViolationsNearProximity(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingViolation.objects.all()
    serializer_class = serializers.GeoParkingViolationSerializer
    class Meta:
        model = ParkingViolation

    def post(self, request, *args, **kwargs):
        raw_queryset = self.get_queryset()
        lat_long = request.POST

        if lat_long == None:
            return Response({'status':'bad request'})

        latitude = float(lat_long['lat'])
        longitude = float(lat_long['long'])

        pnt = Point(longitude, latitude, srid=4326)

        queryset = ParkingViolation.objects.all().values('point', 'violation_code', 'ticket_issue_datetime').filter(point__distance_lte=(pnt, D(m=10)))[:25]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
