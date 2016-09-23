from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import ParkingViolationFine
from django.db.utils import OperationalError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('violation_code').distinct():
                code_name = obj['violation_code']
                data_code_obj, created = ParkingViolationFine.objects.get_or_create(code=code_name)

                # ParkingViolation.objects.select_related('violation_code', 'violation_key').filter(violation_code=code_name, violation_key=None).update(violation_key=data_code_obj)
                remaining_count = True
                while remaining_count:
                    nested_q = ParkingViolation.objects.select_related('violation_code', 'violation_key').filter(violation_code=code_name, violation_key=None)[:10000]
                    if nested_q.count() > 0:
                        print('one batch: %s' % code_name)
                        ParkingViolation.objects.filter(pk__in=nested_q).update(violation_key=data_code_obj)
                    else:
                        remaining_count = False

                self.stdout.write(self.style.SUCCESS(code_name))
