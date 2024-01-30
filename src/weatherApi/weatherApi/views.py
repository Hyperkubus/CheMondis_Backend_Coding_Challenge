from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WeatherData
from .serializers import WeatherDataSerializer
from .services import OpenWeatherMapService


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
def weather_by_city(request, city):
    OWS = OpenWeatherMapService()
    city_data = OWS.geocode(city)
    weather_data = OWS.weatherByLocation(city_data)
    if weather_data['cod'] == 200:
        weather = WeatherData.create_from_openweathermap_data(city_data, weather_data)
        serializer = WeatherDataSerializer(weather, many=False)
        return Response(serializer.data)

    return Response({"error":weather_data["message"]}, status=weather_data["cod"])
