from collections import namedtuple
import csv, os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point

from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles
from api.utils import load_data_csv_to_db
from api.utils import prepare_bulk_loading_of_parking_violations

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--filename', dest='filename', type=str, help="Filename of the csv", required=True)
        parser.add_argument(
            '--url',
            dest='url',
            type=str,
            help='Place url of the csv file',
            required=True
        )

    def handle(self, *args, **options):

        filename = options['filename']
        url = options['url']

        if ParkingViolationDataFiles.objects.filter(url=url):
            raise Exception('Already added file')
        else:
            self.stdout.write(self.style.SUCCESS('Downloading and parsing: %s' % filename))
            parking_violations = load_data_csv_to_db(url, filename)
            self.stdout.write(self.style.SUCCESS('Parsed %s' % filename))

            bulk_objs = prepare_bulk_loading_of_parking_violations(parking_violations)

            # bulk insert
            self.stdout.write(self.style.SUCCESS('Bulk insert of %s' % filename))
            ParkingViolation.objects.bulk_create(bulk_objs, batch_size=10000)

            data_file = ParkingViolationDataFiles(url=url, filename=filename, imported=True)
            data_file.save()

            self.stdout.write(self.style.SUCCESS('Successful insert of %s' % filename))
