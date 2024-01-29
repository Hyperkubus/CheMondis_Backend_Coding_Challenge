from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from json import loads
import requests


def degToDirection(deg):
    deg = deg % 360
    if deg < 45 or deg > 315:
        return 'North'
    if deg < 135:
        return 'East'
    if deg < 225:
        return 'South'
    return 'West'


@api_view(['GET'])
def get_weather(request, city):
    api_key = '74c7c8083e6bffd2eb1efc4f2450b8a7'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    data = requests.get(url).json()
    if data['cod'] == 200:
        weather_data = {
            'City': {
                'city_name': city,
                'latitude': data["coord"]["lat"],
                'longitude': data["coord"]["lon"],
            },
            'Temperature': {
                'current_temperature': data["main"]["temp"],
                'max_temperature': data["main"]["temp_max"],
                'min_temperature': data["main"]["temp_min"],
            },
            'Wind': {
                'wind_speed': data["wind"]["speed"],
                'wind_direction': degToDirection(data["wind"]["deg"]),
            },
            'Air': {
                'humidity': data["main"]["humidity"],
                'pressure': data["main"]["pressure"],
            },
            'Description': data["weather"][0]["description"]
        }

        return Response(weather_data)

    return Response({"error":data["message"]}, status=data["cod"])
