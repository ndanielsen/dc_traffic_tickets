from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('filename').distinct():
                filename = obj['filename']
                data_file_obj = ParkingViolationDataFiles.objects.get(filename=filename)
                ParkingViolation.objects.filter(filename=filename).update(source_filename=data_file_obj)
                self.stdout.write(self.style.SUCCESS(data_file_obj))
