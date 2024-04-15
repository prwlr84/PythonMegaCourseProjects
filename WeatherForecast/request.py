import requests
from dotenv import load_dotenv
import os
from opencage.geocoder import OpenCageGeocode

load_dotenv()

API_KEY = os.getenv('OPENWEATHERAPI')
GEO_KEY = os.getenv('GEO')
geocoder = OpenCageGeocode(GEO_KEY)


def get_city(string):
    if string:
        result = geocoder.geocode(string)
        if result:
            lat = result[0]['geometry']['lat']
            lon = result[0]['geometry']['lng']
            name = result[0]['formatted']

            return {'name': name, 'lat': lat, 'lon': lon}
    else:
        return None


def get_data(lat, lon, days=1):
    nr_values = 8 * days
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    result = requests.get(url)
    content = result.json()['list'][:nr_values]

    return content
