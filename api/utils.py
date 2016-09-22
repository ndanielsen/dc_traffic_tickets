import pandas as pd
from collections import namedtuple
from api.models import ParkingViolation
from api.models import ParkingViolationDataFiles
from django.contrib.gis.geos import Point

# Parking named tuple
Parking = namedtuple('Parking', 'x, y, objectid, rowid, holiday, violation_code, \
                    violation_description, location, rp_plate_state, body_style, \
                    address_id, streetsegid, xcoord, ycoord, filename, \
                    ticket_issue_datetime')

def mil_to_time(x):
    "Convert messy issue_time to datetime object based upon length of issue_time string"
    if x == 'nan':
        return '00:00:00.000Z'

    x = x.split('.')[0]
    lg = len(x)

    if lg == 4:
        t = x[:2] + ':' + x[2:] + ':00.000Z'

    elif lg == 3:
        t = '0' + x[0] + ':' + x[1:] + ':00.000Z'

    elif lg == 2:
        t = '0' + '0' + ':' + x + ':00.000Z'

    elif lg == 1:
        t = '0' + '0' + ':' + '0' + x + ':00.000Z'

    else:
        t = '00:00.000Z'

    # correction for timedate if one element is greater than 5.
    # double check this
    if int(t[3]) > 5:
        t = t[:2]+ ':' + '5' + t[4:]

    return t

def load_data_csv_to_db(url, filename):
    try:
        df = pd.read_csv(url,index_col=None, header=0)
        df.columns = [col.lower() for col in df.columns]
        df = df.reset_index(drop=True)
        df['issue_time_military'] = df.issue_time.apply(str).apply(mil_to_time)
        dates = df.ticket_issue_date.str[:10] + 'T' #+
        df['filename'] = filename
        df['ticket_issue_datetime'] = dates + df.issue_time_military
        df['holiday'] = df.holiday != 0
        df.drop(['day_of_week', 'month_of_year', 'week_of_year', 'issue_time', 'issue_time_military', 'ticket_issue_date'], axis=1, inplace=True, errors='ignore')
        df.drop_duplicates(subset='rowid_', inplace=True)
        df.streetsegid.fillna(0, inplace=True)

        rows = []
        for index, row in df.iterrows():
            row = Parking._make(row)
            rows.append(row)

        return rows
    except:
        print('Some error in the file')

def prepare_bulk_loading_of_parking_violations(parking_violations, url):
    bulk_objs = []
    filename_obj, created = ParkingViolationDataFiles.objects.get_or_create(url=url, filefilename=filename)
    for violation in parking_violations:
        obj = ParkingViolation(
                point = Point((float(violation.x), float(violation.y))),
                objectid = violation.objectid,
                rowid = violation.rowid,
                holiday = violation.holiday,
                violation_code = violation.violation_code,
                violation_description = violation.violation_description,
                address = violation.location,
                rp_plate_state = violation.rp_plate_state,
                body_style = violation.body_style,
                address_id = violation.address_id,
                streetsegid = violation.streetsegid,
                xcoord = violation.xcoord,
                ycoord = violation.ycoord,
                source_filename = filename_obj,
                ticket_issue_datetime = violation.ticket_issue_datetime,
                )
        bulk_objs.append(obj)
    return bulk_objs
