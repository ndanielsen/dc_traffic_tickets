from collections import namedtuple
import csv, os
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point

from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles
from api.utils import load_data_csv_to_db
from api.utils import prepare_bulk_loading_of_parking_violations

class Command(BaseCommand):

    def handle(self, *args, **options):

        file_json = "https://s3.amazonaws.com/dctraffic/dc_parking_violations.json"
        response = requests.get(file_json).json()

        for fullname, csv in response.items():
            url =  csv + '.csv'
            filename = '_'.join(name.lower() for name in fullname.split() ) + '.csv'
            self.load_files_to_db(url, filename)

    def load_files_to_db(self, url, filename):
        if ParkingViolationDataFiles.objects.all().filter(url=url, imported=True):
            self.stdout.write(self.style.INFO('%s already in database' % filename))
        else:
            self.stdout.write(self.style.SUCCESS('Downloading and parsing: %s' % filename))
            parking_violations = load_data_csv_to_db(url, filename)

            if parking_violations is not None:
                self.stdout.write(self.style.SUCCESS('Successful parsing of %s' % filename))

                bulk_objs = prepare_bulk_loading_of_parking_violations(parking_violations)

                # bulk insert
                self.stdout.write(self.style.SUCCESS('Starting bulk create of %s' % filename))
                ParkingViolation.objects.bulk_create(bulk_objs, batch_size=10000)

                data_file = ParkingViolationDataFiles(url=url, filename=filename, imported=True)
                data_file.save()

                self.stdout.write(self.style.SUCCESS('Successful insert of %s' % filename))
            else:
                data_file = ParkingViolationDataFiles(url=url, filename=filename, imported=False)
                data_file.save()
