from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import json

from requests import request

class AuthPTX():
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.version = 'v2'
        self.vehicle = 'Bus'
        self.city = 'Changhua'

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
        
    def request(self, data, params):
        url = f'https://ptx.transportdata.tw/MOTC/{self.version}/{self.vehicle}/{data}'
        response = request('GET', url, params=params, headers=self.get_auth_header())
        return response

import googlemaps
class AuthGooglemap():
    def __init__(self, key):
        self.key = key
    
    def get_geocode(self, address):
        gmaps = googlemaps.Client(key=self.key)
        geocode_result = gmaps.geocode(address)
        location = {
            'lat': geocode_result[0]['geometry']['location']['lat'],
            'lng': geocode_result[0]['geometry']['location']['lng']
        }
        return location

    def distancematrix(self, origins, destinations):
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?"
        params = {
            'origins': origins,
            'destinations': destinations,
            'key': self.key
        }
        response = request("GET", url, params=params)
        result = json.loads(response.content)
        data = result['rows'][0]['elements'][0]['distance']['text']
        return data