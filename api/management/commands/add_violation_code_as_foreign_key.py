from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import ParkingViolationFine

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('violation_code').distinct():
                code_name = obj['violation_code']
                data_code_obj, created = ParkingViolationFine.objects.get_or_create(code=code_name)
                ParkingViolation.objects.filter(violation_code=code_name, violation_key=None).update(violation_key=data_code_obj)
                self.stdout.write(self.style.SUCCESS(code_name))
