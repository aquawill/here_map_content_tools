import argparse

from mapquadlib.herequad import HereQuad

parser = argparse.ArgumentParser()

parser.add_argument('lng', help='longitude, such as 52.52507', type=float)
parser.add_argument("lat", help='latitude, such as 13.36937', type=float)
parser.add_argument("catalog", help='"hdlm" or "rib2"', type=str)
args = parser.parse_args()

lat = args.lat
lng = args.lng
catalog = args.catalog
if catalog == 'hdlm':
    zoom = 14
elif catalog == 'rib2':
    zoom = 12
else:
    print('catalog should be "hdlm" or "rib2"')
    quit()

print(HereQuad.from_lat_lng_level(lat, lng, zoom).long_key)

# example: python lat_lng_to_quad.py 52.52507 13.36937 rib2
