from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import AddressID
from django.db.utils import OperationalError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('address_id').distinct():
                code_name = obj['address_id']
                data_code_obj, created = AddressID.objects.get_or_create(address_id=code_name)

                remaining_count = True
                while remaining_count:
                    nested_q = ParkingViolation.objects.select_related('address_id', 'address_id_key').filter(address_id=code_name, address_id_key=None)[:10000]
                    if nested_q.count() > 0:
                        print('one batch: %s' % code_name)
                        ParkingViolation.objects.filter(pk__in=nested_q).update(address_id_key=data_code_obj)
                    else:
                        remaining_count = False

                self.stdout.write(self.style.SUCCESS(code_name))
