from collections import namedtuple
import csv, os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point

from api.models import ParkingViolation

class Command(BaseCommand):

    def __init__(self):
        self.parking_file = os.path.join(settings.ROOT_DIR.root, 'api/fixtures/parking_violations_sample.csv')
        super(Command, self).__init__()

    def handle(self, *args, **options):
        self.stdout.write(self.parking_file)
        self.stdout.write(self.style.NOTICE('Loading %s' % self.parking_file))

        Parking = namedtuple('Parking', 'x, y, objectid, rowid, holiday, violation_code, \
                            violation_description, location, rp_plate_state, body_style, \
                            address_id, streetsegid, xcoord, ycoord, filename, \
                            ticket_issue_datetime')

        parking_violations = (m for m in map(Parking._make, csv.reader(open(self.parking_file, "rU", encoding='utf-8'), delimiter='\t')))
        for violation in parking_violations:
            try:
                obj = ParkingViolation(
                        point = Point((float(violation.x), float(violation.y))),
                        objectid = violation.objectid,
                        rowid = violation.rowid,
                        holiday = violation.holiday,
                        violation_code = violation.violation_code,
                        violation_description = violation.violation_description,
                        address = violation.location,
                        rp_plate_state = violation.rp_plate_state,
                        body_style = violation.body_style,
                        address_id = violation.address_id,
                        streetsegid = violation.streetsegid,
                        xcoord = violation.xcoord,
                        ycoord = violation.ycoord,
                        filename = violation.filename,
                        ticket_issue_datetime = violation.ticket_issue_datetime,
                        )
                obj.save()
            except ValueError as ex:
                self.stdout.write(self.style.ERROR(violation.rowid))
                self.stdout.write(self.style.ERROR(ex))

            except IntegrityError as ex:
                self.stdout.write(self.style.ERROR(violation.rowid))
                self.stdout.write(self.style.ERROR(ex))

        self.stdout.write(self.style.SUCCESS('Loaded %s' % self.parking_file))
