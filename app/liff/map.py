import googlemaps
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
GOOGLE_MAP_KEY = app.config['GOOGLE_MAP_KEY']

def convert_address(address):
    gmaps = googlemaps.Client(key=GOOGLE_MAP_KEY)
    geocode_result = gmaps.geocode(address)
    return (
        geocode_result[0]['geometry']['location']['lat'],
        geocode_result[0]['geometry']['location']['lng']
    )
