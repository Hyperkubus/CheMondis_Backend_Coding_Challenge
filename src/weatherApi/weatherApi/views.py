import os

from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WeatherData
from .serializers import WeatherDataSerializer
from .services import OpenWeatherMapService

CACHE_TTL = int(os.environ.get("CACHE_TTL", 500))


@api_view(['GET'])
@cache_page(CACHE_TTL)
def weather_by_city(request, city):
    OWS = OpenWeatherMapService()
    city_data = OWS.geocode(city)
    weather_data = OWS.weatherByLocation(city_data)
    if weather_data['cod'] == 200:
        weather = WeatherData.create_from_openweathermap_data(city_data, weather_data)
        serializer = WeatherDataSerializer(weather, many=False)
        return Response(serializer.data)

    return Response({"error": weather_data["message"]}, status=weather_data["cod"])
