from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import PlateState
from django.db.utils import OperationalError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('rp_plate_state').distinct():
                code_name = obj['rp_plate_state']
                data_code_obj, created = PlateState.objects.get_or_create(rp_plate_state=code_name)

                remaining_count = True
                while remaining_count:
                    nested_q = ParkingViolation.objects.select_related('rp_plate_state', 'rp_plate_state_key').filter(rp_plate_state=code_name, rp_plate_state_key=None)[:10000]
                    if nested_q.count() > 0:
                        print('one batch: %s' % code_name)
                        ParkingViolation.objects.filter(pk__in=nested_q).update(rp_plate_state_key=data_code_obj)
                    else:
                        remaining_count = False

                self.stdout.write(self.style.SUCCESS(code_name))
