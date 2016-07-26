from collections import namedtuple
import csv
import os
import zipfile

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point

from api.models import ParkingViolation

class Command(BaseCommand):

    def __init__(self):
        self.parking_file_zip = os.path.join(settings.ROOT_DIR.root, 'api/fixtures/parking_violations.zip')
        self.parking_file_upzipped = 'parking_violations.csv'
        super(Command, self).__init__()

    def handle(self, *args, **options):

        if not os.path.isfile(self.parking_file_zip):

            self.stdout.write(self.style.ERROR('Warning, this might take awhile dependin on your internet connection'))

            with open(self.parking_file_zip, 'wb') as handle:
                response = requests.get('https://s3.amazonaws.com/dctraffic/parking_violations.zip', stream=True)

                if not response.ok:
                    # Something went wrong
                    self.stdout.write(self.style.ERROR('ERROR'))

                for block in response.iter_content(1024):

                    handle.write(block)

            self.stdout.write(self.style.SUCCESS('Downloaded %s' % self.parking_file_zip))

        else:
            self.stdout.write(self.style.SUCCESS('File exists: %s' % self.parking_file_zip))

        Parking = namedtuple('Parking', 'x, y, objectid, rowid, holiday, violation_code, \
                            violation_description, location, rp_plate_state, body_style, \
                            address_id, streetsegid, xcoord, ycoord, filename, \
                            ticket_issue_datetime')

        with zipfile.ZipFile(self.parking_file_zip) as z:
            with z.open(self.parking_file_upzipped, 'rU') as f:
                for line in f:
                    try:
                        # print(dir(f))
                        l = line.decode("utf-8").replace('\n', '').split(',')
                        violation = Parking._make(l)
                        # break

                        print(violation.objectid)

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
                        # self.stdout.write(self.style.ERROR(violation.rowid))
                        # self.stdout.write(self.style.ERROR(ex))
                        pass

                    except IntegrityError as ex:
                        # self.stdout.write(self.style.ERROR(violation.rowid))
                        # self.stdout.write(self.style.ERROR(ex))
                        pass

                    except TypeError as ex:
                        # self.stdout.write(self.style.ERROR(violation.rowid))
                        # self.stdout.write(self.style.ERROR(ex))
                        pass

        self.stdout.write(self.style.SUCCESS('Loaded %s' % self.parking_file_upzipped))
