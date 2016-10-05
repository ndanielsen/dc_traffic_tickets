from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('migrate')
        call_command('add_violation_code_as_foreign_key')
        call_command('add_filename_as_foreign_key')
        call_command('add_streetid_as_foreign_key')
        call_command('add_addressid_as_foreign_key')
        call_command('add_bodystyleid_as_foreign_key')
        call_command('add_platestateid_as_foreign_key')
