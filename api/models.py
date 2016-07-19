from __future__ import unicode_literals

from django.contrib.gis.db import models

class ParkingViolation(models.Model):
    """
    Model for a parking violation
    """
    class Meta:
        verbose_name_plural = "Parking Violations"

    location = models.PointField()
    objectid = models.IntegerField()
    rowid = models.IntegerField(unique=True)
    holiday = models.BooleanField()
    violation_code = models.CharField(max_length=10)
    violation_description = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    rp_plate_state = models.CharField(max_length=5)
    body_style = models.CharField(max_length=5)
    address_id = models.IntegerField()
    streetsegid = models.FloatField()
    xcoord = models.IntegerField()
    ycoord = models.IntegerField()
    filename = models.CharField(max_length=50)
    ticket_issue_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.ticket_issue_datetime)
