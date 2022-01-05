import numpy as np
import pandas as pd
import requests
import json

sg_api = '<your-api-key>'

def lat_lon_pk(loc_name, lat, lon):
    headers = {
        'apikey': cc_sg_api,
        'content-type': 'application/json',
    }

    location_name = loc_name
    latitude = str(lat)
    longitude = str(lon)
    iso_country_code = 'US'

    cols = [
        'location_name',
        'street_address',
        'latitude',
        'longitude',
        'postal_code'
    ]
    cols = ' '.join(cols)

    lookup = '''
        lookup(query: {
        location_name: \\"%s\\",
        latitude: %s,
        longitude: %s,
        iso_country_code: \\"%s\\"})
    '''
    lookup = lookup % (location_name, latitude, longitude, iso_country_code)
    lookup = lookup.strip().replace('\n', '')

    data = '{"query": "query {%s {placekey safegraph_core {%s}}}", "variables":{}}'
    response = requests.post('https://api.safegraph.com/v1/graphql',
                             headers=headers,
                             data=data % (lookup, cols))
    sg_records_num = json.loads("".join(response.text))['extensions']['row_count']
    if sg_records_num > 0:
        print(f'{sg_records_num} sg place found.')
        return (json.loads("".join(response.text))['data']['lookup']['placekey'],
                json.loads("".join(response.text))['data']['lookup']['safegraph_core']['latitude'],
                json.loads("".join(response.text))['data']['lookup']['safegraph_core']['longitude'])
    else:
        print('No record found.')
        return np.nan, np.nan, np.nan


def lookup_pk_sgname(pk):
    headers = {
        'apikey': cc_sg_api,
        'content-type': 'application/json',
    }

    placekey = pk
    lookup = 'lookup(placekey: \\"{}\\")'.format(placekey)
    cols = [
        'placekey',
        'latitude',
        'longitude',
        'street_address',
        'location_name'
    ]
    cols = ' '.join(cols)
    data = '{"query": "query {%s {safegraph_core {%s}}}", "variables":{}}'
    response = requests.post('https://api.safegraph.com/v1/graphql',
                            headers=headers,
                            data=data % (lookup, cols))
    return json.loads(
            "".join(response.text)
        )['data']['lookup']['safegraph_core']['location_name']
