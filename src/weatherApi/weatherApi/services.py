import os
import requests
import aiohttp
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

    async def __request(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                if response.status == 401:
                    raise NotAuthenticated()
                if response.status == 404:
                    raise NotFound()
                if response.status == 429:
                    raise Throttled()
                if response.status >= 500:
                    raise APIException(code=response.status, detail=response)
                raise APIException()

    async def geocode(self, location: str, limit: int = 1, lang='en'):
        request_url = f'{self.base_url}/geo/1.0/direct?q={location}&limit={limit}&appid={self.apikey}'
        data = await self.__request(request_url)
        if len(data) == 0:
            raise NotFound()
        if 'lat' not in data[0].keys() or 'lon' not in data[0].keys():
            raise ValidationError()
        if "local_names" in data[0].keys():
            if lang in data[0]['local_names'].keys():
                print(data[0]['local_names'][lang])
                return self.City(data[0]['local_names'][lang], data[0]['lat'], data[0]['lon'])
        return self.City(data[0]['name'], data[0]['lat'], data[0]['lon'])

    async def weatherByLocation(self, location: City, units='metric', lang='en'):
        request_url = f'{self.base_url}/data/2.5/weather?lat={location.lat}&lon={location.lon}&units={units}&lang={lang}&appid={self.apikey}'
        return await self.__request(request_url)

    async def weatherByCity(self, city: str):
        location = await self.geocode(location=city)
        return await self.weatherByLocation(location=location)