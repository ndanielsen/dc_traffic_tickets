import csv, os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.contrib.gis.geos import Point
from django.test.utils import override_settings

from api.models import ParkingViolationFine

class Command(BaseCommand):

    def __init__(self):
        self.fine_file = os.path.join(settings.ROOT_DIR.root, 'api/fixtures/fines.csv')
        super(Command, self).__init__()

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            self.stdout.write(self.fine_file)
            self.stdout.write(self.style.NOTICE('Loading %s' % self.fine_file))

            with open(self.fine_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                list_of_fines = list(reader)

                # CODE,DESC,SHORTDESC,FINE

            fine_map = {"CODE":"violation_code", "DESC":"description", "SHORTDESC":'short_description', "FINE":'fine'}
            map_func = lambda row: {fine_map[key]: value for key, value in row.items()}
            mapped_fines = map(map_func, list_of_fines )

            def add_null_func(x):
                x['json_data'] = {'empty': True}
                return x

            mapped_fines = map(add_null_func, mapped_fines )
            create_func = lambda x: ParkingViolationFine.objects.update_or_create(violation_code=x['violation_code'], defaults=x)
            create_map = map(create_func, mapped_fines)
            list(create_map)

            self.stdout.write(self.style.SUCCESS('Loaded %s' % self.fine_file))
