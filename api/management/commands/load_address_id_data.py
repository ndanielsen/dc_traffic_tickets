import os
import csv

from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from django.test.utils import override_settings
from django.contrib.gis.geos import Point
from django.db.utils import OperationalError
from django.db import models
from django.conf import settings

from api.models import ParkingViolation
from api.models import ParkingViolationFine
from api.models import AddressID

"""<U+FEFF>X,Y,OBJECTID_12,SITE_ADDRESS_PK,ADDRESS_ID,STATUS,SSL,TYPE_,
ENTRANCETYPE,ADDRNUM,ADDRNUMSUFFIX,STNAME,STREET_TYPE,QUADRANT,CITY,STATE,
FULLADDRESS,SQUARE,SUFFIX,LOT,NATIONALGRID,ASSESSMENT_NBHD,ASSESSMENT_SUBNBHD,
CFSA_NAME,HOTSPOT,CLUSTER_,POLDIST,ROC,PSA,SMD,CENSUS_TRACT,VOTE_PRCNCT,WARD,
ZIPCODE,ANC,NEWCOMMSELECT06,NEWCOMMCANDIDATE,CENSUS_BLOCK,CENSUS_BLOCKGROUP,
FOCUS_IMPROVEMENT_AREA,SE_ANNO_CAD_DATA,LATITUDE,LONGITUDE,ACTIVE_RES_UNIT_COUNT,
RES_TYPE,ACTIVE_RES_OCCUPANCY_COUNT,WARD_2002,WARD_2012,ANC_2002,ANC_2012,SMD_2002,SMD_2012"""

### Ignored fields (probably empty)
#     # "FOCUS_IMPROVEMENT_AREA": 'focus_improvement_area', # bool?


mapping = {"STATUS": 'official_status', # string
    "ADDRESS_ID":"address_id",
    "ADDRNUM" : 'address_num', #str
    "ADDRNUMSUFFIX": 'address_suffix', #str
    "ANC": "advisory_neighborhood_commission",
    "STNAME": 'street_name',# str
    "STREET_TYPE": 'street_type', #str
    "QUADRANT": 'quadrant', #str
    "LONGITUDE": 'longitude',
    "LATITUDE":'latitude',
    "ASSESSMENT_NBHD": 'neighbor_hood', #str
    "CLUSTER_": 'neighbor_hood_cluster',  #('parse to just have number remaining')
    "POLDIST": 'police_district', #
    "PSA": 'police_service_area', # police_service_area
    "SMD": 'single_member_district', # single_member_district
    "CENSUS_TRACT": 'census_tract', # int
    "VOTE_PRCNCT": 'vote_precinct', # ('parse out words') # int
    "WARD": 'ward', # (parse out words) # int
    "ZIPCODE": 'zipcode', #zipcode field
    "CENSUS_BLOCK": 'census_block', # int?
    "CENSUS_BLOCKGROUP": 'census_blockgroup', # int?
    "RES_TYPE": 'residential_type', # residential_type
    "ACTIVE_RES_OCCUPANCY_COUNT": 'resident_occupancy_count', # int
    }

def clean_model_inputs(x):
    x['vote_precinct'] = x['vote_precinct'].replace('Precinct', '') # "Precinct" # int
    x['neighbor_hood_cluster'] = x['neighbor_hood_cluster'].replace('Cluster', '')
    x['police_service_area'] = x['police_service_area'].replace('Police Service Area', '') # 'Police Service Area'
    x['police_district'] = x['police_district'].replace("Police District -", '')
    x['single_member_district'] = x['single_member_district'].replace('SMD', '') # SMD
    x['advisory_neighborhood_commission'] = x['advisory_neighborhood_commission'].replace('ANC', '')
    x['ward'] = x['ward'].replace('Ward', '')
    x['census_block'] = x['census_block'].replace(' ', '-')
    x['census_blockgroup'] = x['census_blockgroup'].replace(' ', '-')
    x = {key: value.lower().strip() for key, value in x.items() if not isinstance(value, dict)}
    return x

def cast_model_inputs(x):
    x['neighbor_hood_cluster'] = clean_int_casting(x, 'neighbor_hood_cluster')
    x['address_id'] = clean_int_casting(x, 'address_id')
    x['vote_precinct'] = clean_int_casting(x, 'vote_precinct')
    x['resident_occupancy_count'] = clean_int_casting(x, 'resident_occupancy_count')
    x['ward'] = clean_int_casting(x, 'ward')
    x['census_tract'] = clean_int_casting(x, 'census_tract')
    x['police_service_area'] = clean_int_casting(x, 'police_service_area')
    return x

def clean_int_casting(dict, key):
    return int(dict[key]) if dict[key] != '' else None


json_fields = set(
    ["SQUARE",
    "LOT",
    "WARD_2002", # ForeignKey to ward with year
    "WARD_2012",# ForeignKey to ward with year
    "ANC_2002", # ForeignKey to anc with year
    "ANC_2012", # ForeignKey to anc with year
    "SMD_2002", # ForeignKey to single_member_district with year
    "SMD_2012" # ForeignKey to single_member_district with year
    "ASSESSMENT_SUBNBHD", # str
    "CFSA_NAME", # str
    ])

ADDRESSID_FIELDS = set([f.name for f in AddressID._meta.get_fields()])

def model_mapping_func(x):
    y = {mapping[key]: val for key, val in x.items() if key in mapping.keys()}
    y.update({'json_data': {key: val for key, val in x.items() if key in json_fields}})
    return y

def add_django_objs_func(x):
    x['point'] = Point((float(x['longitude']), float(x['latitude'])))
    return x

def update_model(x):
    x = {key: value for key, value in x.items() if key in ADDRESSID_FIELDS }
    obj, created = AddressID.objects.update_or_create(address_id=x['address_id'], defaults=x)
    return created


class Command(BaseCommand):

    def handle(self, *args, **options):
        with override_settings(CACHALOT_ENABLED=False):
            self.stdout.write(self.style.NOTICE('Starting loading'))
            filename = os.path.join(settings.ROOT_DIR.root, 'api/fixtures/dc_address_points.csv')

            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                mappings = map(model_mapping_func, reader)
                cleaned_mappings = map(clean_model_inputs, mappings)
                casted_mappings = map(cast_model_inputs, cleaned_mappings)
                obj_mappings = map(add_django_objs_func, casted_mappings)
                updated_or_created = map(update_model, obj_mappings)
                new_objs = list(updated_or_created)

            self.stdout.write(self.style.SUCCESS('%s address_ids created' % len(new_objs)))
