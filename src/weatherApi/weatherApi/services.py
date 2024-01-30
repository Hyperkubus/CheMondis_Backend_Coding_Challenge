import os
import requests


class OpenWeatherMapService(object):
    apikey: str = None
    base_url: str = 'http://api.openweathermap.org'

    class City:
        name: str = None
        lat: float = None
        lon: float = None

        def __init__(self, city: str, lat: float, lon: float):
            self.name = city
            self.lat = lat
            self.lon = lon

    def __init__(self):
        self.apikey = os.environ['OPENWEATHERMAP_API_KEY']

    def request(self, url: str):
        response = requests.get(url)
        if (response.status_code == 200):
            return response.json()
        if (response.status_code == 401):
            raise Exception('Invalid API key', response.status_code)
        if (response.status_code == 404):
            raise Exception('Not Found', response.status_code)
        if (response.status_code == 429):
            raise Exception('Rate Limit Reached', response.status_code)
        if (response.status_code >= 500):
            raise Exception('Server Error', response.status_code)
        raise Exception('Unexpected Error')

    def geocode(self, location: str, limit: int = 1):
        request_url = f'{self.base_url}/geo/1.0/direct?q={location}&limit={limit}&appid={self.apikey}'
        data = self.request(request_url)
        if len(data) == 0:
            raise Exception('Location not found', location)
        if 'lat' not in data[0].keys() or 'lon' not in data[0].keys():
            raise Exception('Response is missing keys', data[0].keys)
        return self.City(data[0]['name'], data[0]['lat'], data[0]['lon'])

    def weatherByLocation(self, location: City, units='metric'):
        request_url = f'{self.base_url}/data/2.5/weather?lat={location.lat}&lon={location.lon}&units={units}&appid={self.apikey}'
        return self.request(request_url)

    def weatherByCity(self, city: str):
        location = self.geocode(location=city)
        return self.weatherByLocation(location=location)