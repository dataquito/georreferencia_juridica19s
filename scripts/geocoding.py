import requests
import pandas as pn
import unidecode

def get_geocoding(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = ''
    if len(results) > 0:
        location = results[0]['geometry']['location']
        location = location['lat'], location['lng']

    print location
    return location

file_to_read = 'base_juridica.xlsx'
column_to_process = u'Ubicación del inmueble/edificio/casa dañado (calle, número, ciudad, CP, estado)'
file_to_write = 'base_juridica_georef_2.xlsx'

df = pn.read_excel(file_to_read)
column_intermedia = df[column_to_process].map(lambda x: get_geocoding(unidecode.unidecode(x)) if not(pn.isnull(x)) else '')
df['lat'] = column_intermedia.apply(lambda x: x[0] if x else '')
df['long'] = column_intermedia.apply(lambda x: x[1] if x else '')
df.to_excel(file_to_write)
