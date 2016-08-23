from __future__ import unicode_literals

from django.contrib.gis.db import models

class ParkingViolation(models.Model):
    """
    Model for a parking violation
    """
    class Meta:
        verbose_name_plural = "Parking Violations"

    point = models.PointField()
    objectid = models.IntegerField()
    rowid = models.IntegerField(unique=True)
    holiday = models.BooleanField()
    violation_code = models.CharField(max_length=10, db_index=True)
    violation_description = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    rp_plate_state = models.CharField(max_length=5, db_index=True)
    body_style = models.CharField(max_length=5, db_index=True)
    address_id = models.IntegerField()
    streetsegid = models.FloatField()
    xcoord = models.IntegerField()
    ycoord = models.IntegerField()
    filename = models.CharField(max_length=50)
    ticket_issue_datetime = models.DateTimeField(db_index=True)

    def __str__(self):
        return str(self.ticket_issue_datetime)
