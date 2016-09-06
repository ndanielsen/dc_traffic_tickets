from collections import namedtuple
import csv, os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point

from api.models import ParkingViolation

class Command(BaseCommand):

    def handle(self, *args, **options):
        lastSeenId = float('-Inf')
        rows = ParkingViolation.objects.all().order_by('objectid')
        count = 0
        self.stdout.write(self.style.SUCCESS("looking for dups"))
        for row in rows:
            if row.objectid == lastSeenId:
                count += 1
                row.delete() # We've seen this id in a previous row
            else: # New id found, save it and check future rows for duplicates.
                lastSeenId = row.objectid
            print(count)

        self.stdout.write(self.style.SUCCESS("Founds %s" % count))
