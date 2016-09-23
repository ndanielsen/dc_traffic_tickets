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

                ParkingViolation.objects.select_related('violation_code', 'violation_key').filter(violation_code=code_name, violation_key=None).update(violation_key=data_code_obj)
                # for chunk in chunked_queryset(ParkingViolation.objects.select_related('violation_code', 'violation_key').filter(violation_code=code_name, violation_key=None), 5000):
                    # chunk.update(violation_key=data_code_obj)

                self.stdout.write(self.style.SUCCESS(code_name))


def chunked_queryset(qs, batch_size, index='id'):
    """
    Yields a queryset split into batches of maximum size 'batch_size'.
    Any ordering on the queryset is discarded.
    """
    qs = qs.order_by()  # clear ordering
    min_max = qs.aggregate(min=models.Min(index), max=models.Max(index))
    min_id, max_id = min_max['min'], min_max['max']
    if max_id is not None:
        for i in range(min_id, max_id + 1, batch_size):
            filter_args = {'{0}__range'.format(index): (i, i + batch_size - 1)}
            yield qs.filter(**filter_args)
