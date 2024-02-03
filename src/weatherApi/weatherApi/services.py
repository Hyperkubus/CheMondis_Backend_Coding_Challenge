import os
import requests
from rest_framework.exceptions import NotAuthenticated, NotFound, Throttled, APIException, ValidationError, \
    NotAcceptable


class OpenWeatherMapService(object):
    __instance = None

    apikey: str = None
    base_url: str = 'http://api.openweathermap.org'

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(OpenWeatherMapService, cls).__new__(cls)
        return cls.__instance

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

    def __request(self, url: str):
        response = requests.get(url)
        if (response.status_code == 200):
            return response.json()
        if (response.status_code == 401):
            raise NotAuthenticated()
        if (response.status_code == 404):
            raise NotFound()
        if (response.status_code == 429):
            raise Throttled()
        if (response.status_code >= 500):
            raise APIException(code=response.status_code, detail=response)
        raise APIException()

    def geocode(self, location: str, limit: int = 1, lang='en'):
        request_url = f'{self.base_url}/geo/1.0/direct?q={location}&limit={limit}&appid={self.apikey}'
        data = self.__request(request_url)
        if len(data) == 0:
            raise NotFound()
        if 'lat' not in data[0].keys() or 'lon' not in data[0].keys():
            raise ValidationError()
        if "local_names" in data[0].keys():
            if lang in data[0]['local_names'].keys():
                print(data[0]['local_names'][lang])
                return self.City(data[0]['local_names'][lang], data[0]['lat'], data[0]['lon'])
        return self.City(data[0]['name'], data[0]['lat'], data[0]['lon'])

    def weatherByLocation(self, location: City, units='metric', lang='en'):
        request_url = f'{self.base_url}/data/2.5/weather?lat={location.lat}&lon={location.lon}&units={units}&lang={lang}&appid={self.apikey}'
        return self.__request(request_url)

    def weatherByCity(self, city: str):
        location = self.geocode(location=city)
        return self.weatherByLocation(location=location)