from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings

from api.models import ParkingViolation
from api.models import BodyStyle
from django.db.utils import OperationalError
from django.db import models

class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            for obj in ParkingViolation.objects.values('body_style').distinct():
                code_name = obj['body_style']
                data_code_obj, created = BodyStyle.objects.get_or_create(body_style=code_name)

                remaining_count = True
                while remaining_count:
                    nested_q = ParkingViolation.objects.select_related('body_style', 'body_style_key').filter(body_style=code_name, body_style_key=None)[:10000]
                    if nested_q.count() > 0:
                        print('one batch: %s' % code_name)
                        ParkingViolation.objects.filter(pk__in=nested_q).update(body_style_key=data_code_obj)
                    else:
                        remaining_count = False

                self.stdout.write(self.style.SUCCESS(code_name))
