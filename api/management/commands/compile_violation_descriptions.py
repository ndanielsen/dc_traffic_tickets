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
                data_code_obj = ParkingViolation.objects.values_list('violation_description', flat=True).filter(violation_code=code_name).distinct()

                fine_obj = ParkingViolationFine.objects.get(pk=code_name)
                fine_obj.json_data['compile_description'] = ", ".join(item for item in list(data_code_obj))
                try:
                    del fine_obj.json_data['empty']
                except:
                    pass
                fine_obj.save()

                self.stdout.write(self.style.SUCCESS(code_name))
