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
    objectid = models.IntegerField()
    rowid = models.IntegerField() #unique=True)
    holiday = models.BooleanField()
    violation_code = models.CharField(max_length=10, db_index=True)
    violation_key = models.ForeignKey('ParkingViolationFine', on_delete=models.CASCADE, blank=True, null=True,)

    violation_description = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    rp_plate_state = models.CharField(max_length=5, db_index=True)
    body_style = models.CharField(max_length=5, db_index=True)
    address_id = models.IntegerField()
    streetsegid = models.FloatField()
    xcoord = models.IntegerField()
    ycoord = models.IntegerField()
    filename = models.CharField(max_length=50, db_index=True)
    source_filename = models.ForeignKey('ParkingViolationDataFiles', on_delete=models.CASCADE, blank=True, null=True,)
    ticket_issue_datetime = models.DateTimeField(db_index=True)

    def __str__(self):
        return str(self.ticket_issue_datetime)

class ParkingViolationDataFiles(models.Model):
    class Meta:
        verbose_name_plural = "Source Datasets - Parking Violations"

    filename = models.CharField(max_length=100, blank=False)
    url = models.URLField(blank=False, )
    imported = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.filename)

class ParkingViolationFine(models.Model):
    class Meta:
        verbose_name_plural = "Parking Violations Fines"

    code = models.CharField(max_length=10, db_index=True)
    description = models.CharField(max_length=100, blank=False, null=True,)
    short_description = models.CharField(max_length=50, blank=False, null=True,)
    fine = models.FloatField(blank=True, null=True,)

    def __str__(self):
        return str(self.code)


        # CODE,DESC,SHORTDESC,FINE
