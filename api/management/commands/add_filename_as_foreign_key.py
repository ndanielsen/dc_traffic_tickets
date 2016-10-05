from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles
from django.db.utils import OperationalError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('filename').distinct():
                code_name = obj['filename']
                data_code_obj, created = ParkingViolationDataFiles.objects.get_or_create(filename=code_name)

                remaining_count = True
                while remaining_count:
                    nested_q = ParkingViolation.objects.select_related('filename', 'source_filename').filter(filename=code_name, source_filename=None)[:10000]
                    if nested_q.count() > 0:
                        print('one batch: %s' % code_name)
                        ParkingViolation.objects.filter(pk__in=nested_q).update(source_filename=data_code_obj)
                    else:
                        remaining_count = False

                self.stdout.write(self.style.SUCCESS(code_name))
