import requests
import zipfile
import os
from clint.textui import progress

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Downloads all geojson files in DC Open Data and adds them to static files in dataviz"

    def handle(self, *args, **options):
        self.dc_geo_maps_file = os.path.join(settings.ROOT_DIR.root, 'dataviz/static/data.zip')
        self.dataviz_static_folder = os.path.join(settings.ROOT_DIR.root, 'dataviz/static/')
        if not os.path.isfile(self.dc_geo_maps_file):
            self.stdout.write(self.style.ERROR('Warning, this might take awhile depending on your internet connection'))
            response = requests.get('https://s3.amazonaws.com/dctraffic/data.zip', stream=True)

            if not response.ok:
                # Something went wrong
                self.stdout.write(self.style.ERROR('ERROR'))

            else:
                self.stdout.write(self.style.SUCCESS('Downloading %s' % self.dc_geo_maps_file))
                with open(self.dc_geo_maps_file, 'wb') as handle:
                    total_length = int(response.headers.get('content-length')) / 1024 + 1
                    # Override the expected_size, for iterables that don't support len()
                    for block in progress.bar(response.iter_content(1024), expected_size=total_length):
                        handle.write(block)
                        handle.flush()

                self.stdout.write(self.style.SUCCESS('Finished Download %s' % self.dc_geo_maps_file))
        if os.path.isfile(self.dc_geo_maps_file):
            zfile = zipfile.ZipFile(self.dc_geo_maps_file)
            zfile.extractall(self.dataviz_static_folder)
            self.stdout.write(self.style.SUCCESS('Unzipped all files in %s' % self.dc_geo_maps_file))

            # Small file so don't remove
            # os.remove(self.dc_geo_maps_file)
