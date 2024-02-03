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
    request_language = request.query_params['lang'] or "en"
    OWM_service = OpenWeatherMapService()
    city_data = OWM_service.geocode(city)
    weather_data = OWM_service.weatherByLocation(city_data,lang=request_language)
    if weather_data['cod'] == 200:
        weather = WeatherData.create_from_openweathermap_data(city_data, weather_data)
        serializer = WeatherDataSerializer(weather, many=False)
        return Response(serializer.data)

    return Response({"error": weather_data["message"]}, status=weather_data["cod"])
