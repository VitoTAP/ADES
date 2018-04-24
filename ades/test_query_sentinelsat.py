import sentinelsat


import json
from sentinelsat import SentinelAPI
import geojson
from shapely.geometry import shape

with open("resources/canada.geojson", 'r+') as file:
    nwt = geojson.load(file)["features"][0]

"""
Some sample code to construct the OpenSearch Query for our products.
"""
simplified = shape(nwt.geometry).simplify(0.5, preserve_topology=False)
print(simplified.to_wkt())
api = SentinelAPI('test', 'test')
query = api.format_query(date=("20170617", "20170628"), producttype='SLC',platformname='Sentinel-1',polarisationmode='HH HV',orbitdirection='DESCENDING',
                         geometry=simplified.to_wkt())

print(query)

products = api.query(simplified.to_wkt(),date=("20170617", "20170628"),producttype='SLC', platformname='Sentinel-1',orbitdirection='DESCENDING',polarisationmode='HH HV')