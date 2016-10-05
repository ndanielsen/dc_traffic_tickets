from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

class ParkingViolation(models.Model):
    """
    Model for a parking violation
    """
    class Meta:
        verbose_name_plural = "Parking Violations"
        index_together = [ ["id", "ticket_issue_datetime"], ]

    point = models.PointField()
    objectid = models.IntegerField(blank=True, null=True)
    rowid = models.IntegerField(blank=True, null=True) #unique=True)
    holiday = models.BooleanField()
    violation_code = models.ForeignKey('ParkingViolationFine', on_delete=models.SET_NULL, blank=True, null=True,)
    violation_description = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    rp_plate_state = models.ForeignKey('PlateState', on_delete=models.SET_NULL, blank=True, null=True,)
    body_style = models.ForeignKey('BodyStyle', on_delete=models.SET_NULL, blank=True, null=True,)
    address_id = models.ForeignKey('AddressID', on_delete=models.SET_NULL, blank=True, null=True,)
    streetsegid = models.ForeignKey('StreetSegID', on_delete=models.SET_NULL, blank=True, null=True,)

    xcoord = models.IntegerField(blank=True, null=True)
    ycoord = models.IntegerField(blank=True, null=True)
    data_filename = models.ForeignKey('ParkingViolationDataFiles', on_delete=models.SET_NULL, blank=True, null=True,)
    ticket_issue_datetime = models.DateTimeField(db_index=True)

    def __str__(self):
        return str(self.ticket_issue_datetime)

    @property
    def longitude(self):
        return self.point.x

    @property
    def latitude(self):
        return self.point.y


class ParkingViolationDataFiles(models.Model):
    class Meta:
        verbose_name_plural = "Source Datasets - Parking Violations"

    filename = models.CharField(max_length=100, null=True, blank=False, db_index=True)
    url = models.URLField(null=True, blank=False )
    imported = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename)

class ParkingViolationFine(models.Model):
    class Meta:
        verbose_name_plural = "Parking Violations Fines"

    violation_code = models.CharField(max_length=10, db_index=True, blank=False, null=True,)
    description = models.CharField(max_length=100, blank=False, null=True,)
    short_description = models.CharField(max_length=50, blank=False, null=True,)
    json_data = JSONField(default={})
    fine = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return str(self.violation_code)

class StreetSegID(models.Model):
    class Meta:
        verbose_name_plural = "Street Segment IDs"

    streetsegid = models.FloatField(db_index=True, blank=False, null=True,)
    def __str__(self):
        return str(self.streetsegid)

class AddressID(models.Model):
    class Meta:
        verbose_name_plural = "Address IDs"
        index_together = [ ["id", "address_id"], ["census_tract", "census_blockgroup", "census_block"] ]

    address_id = models.IntegerField(db_index=True, blank=False, null=True,)
    point = models.PointField(null=True, blank=True)
    json_data = JSONField(default={})

    official_status = models.CharField(max_length=100, blank=False, null=True, db_index=True)
    residential_type = models.CharField(max_length=20, blank=False, null=True,)
    neighbor_hood = models.CharField(max_length=100, blank=False, null=True,)
    neighbor_hood_cluster = models.IntegerField(blank=False, null=True, db_index=True)
    vote_precinct = models.IntegerField(blank=False, null=True, db_index=True)
    single_member_district = models.CharField(max_length=10, blank=False, null=True, db_index=True)
    advisory_neighborhood_commission = models.CharField(max_length=10, blank=False, null=True, db_index=True)

    resident_occupancy_count = models.IntegerField(blank=False, null=True,)
    ward = models.IntegerField(blank=False, null=True, db_index=True)

    census_tract = models.IntegerField(blank=False, null=True, db_index=True)
    census_blockgroup = models.CharField(max_length=15, blank=False, null=True, db_index=True)
    census_block = models.CharField(max_length=15, blank=False, null=True, db_index=True)

    address_num = models.CharField(max_length=10, blank=False, null=True,)
    street_type = models.CharField(max_length=10, blank=False, null=True,)
    street_name = models.CharField(max_length=40, blank=False, null=True,)
    address_suffix = models.CharField(max_length=10, blank=False, null=True,)
    quadrant = models.CharField(max_length=2, db_index=True)
    zipcode = models.CharField(max_length=20, db_index=True)

    police_district = models.CharField(max_length=100, blank=False, null=True,)
    police_service_area = models.IntegerField(blank=False, null=True,)

    def __str__(self):
        return str(self.address_id)

class BodyStyle(models.Model):
    class Meta:
        verbose_name_plural = "Body Styles"

    body_style = models.CharField(db_index=True, max_length=20, blank=False, null=True,)

    def __str__(self):
        return str(self.body_style)

class PlateState(models.Model):
    class Meta:
        verbose_name_plural = "Reported Plate States"

    rp_plate_state = models.CharField(db_index=True, max_length=10, blank=False, null=True,)

    def __str__(self):
        return str(self.rp_plate_state)


# new models
#
# Ward
# SingleMemberDistrict
# AdvisoryNeighborhoodCommission


# police district
