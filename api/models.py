from __future__ import unicode_literals

from django.contrib.gis.db import models

class ParkingViolation(models.Model):
    """
    Model for a parking violation
    """
    class Meta:
        verbose_name_plural = "Parking Violations"
        index_together = [ ["violation_key", "violation_code"], ['filename','source_filename']]

    point = models.PointField()

    objectid = models.IntegerField(blank=True, null=True)
    rowid = models.IntegerField(blank=True, null=True) #unique=True)
    holiday = models.BooleanField()

    violation_code = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    violation_key = models.ForeignKey('ParkingViolationFine', on_delete=models.CASCADE, blank=True, null=True,)

    violation_description = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)

    rp_plate_state = models.CharField(max_length=5, db_index=True)
    rp_plate_state_key = models.ForeignKey('PlateState', on_delete=models.CASCADE, blank=True, null=True,)

    body_style = models.CharField(max_length=5, db_index=True)
    body_style_key = models.ForeignKey('BodyStyle', on_delete=models.CASCADE, blank=True, null=True,)

    address_id = models.IntegerField(blank=True, null=True)
    address_id_key = models.ForeignKey('AddressID', on_delete=models.CASCADE, blank=True, null=True,)

    streetsegid = models.FloatField(blank=True, null=True)
    streetsegid_key = models.ForeignKey('StreetSegID', on_delete=models.CASCADE, blank=True, null=True,)

    xcoord = models.IntegerField(blank=True, null=True)
    ycoord = models.IntegerField(blank=True, null=True)
    filename = models.CharField(max_length=50, db_index=True,  blank=True, null=True,)
    source_filename = models.ForeignKey('ParkingViolationDataFiles', on_delete=models.CASCADE, blank=True, null=True,)
    ticket_issue_datetime = models.DateTimeField(db_index=True)

    def __str__(self):
        return str(self.ticket_issue_datetime)

class ParkingViolationDataFiles(models.Model):
    class Meta:
        verbose_name_plural = "Source Datasets - Parking Violations"

    filename = models.CharField(max_length=100, null=True, blank=False)
    url = models.URLField(null=True, blank=False )
    imported = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename)

class ParkingViolationFine(models.Model):
    class Meta:
        verbose_name_plural = "Parking Violations Fines"

    code = models.CharField(max_length=10, db_index=True, blank=False, null=True,)
    description = models.CharField(max_length=100, blank=False, null=True,)
    short_description = models.CharField(max_length=50, blank=False, null=True,)
    fine = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return str(self.code)

class StreetSegID(models.Model):
    class Meta:
        verbose_name_plural = "Street Segment IDs"

    streetsegid = models.FloatField(db_index=True, blank=False, null=True,)

    def __str__(self):
        return str(self.streetsegid)

class AddressID(models.Model):
    class Meta:
        verbose_name_plural = "Address IDs"

    address_id = models.IntegerField(db_index=True, blank=False, null=True,)

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
