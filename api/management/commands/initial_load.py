from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


from api.models import ParkingViolation

class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('load_dc_data', 'parking')

        call_command('loaddata', 'fixture.json')

        self.stdout.write(self.style.SUCCESS('Auth Set Up'))
