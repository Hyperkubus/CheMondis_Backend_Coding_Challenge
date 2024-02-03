import os

from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WeatherData
from .serializers import WeatherDataSerializer
from .services import OpenWeatherMapService

from django.utils.translation import gettext as _

CACHE_TTL = int(os.environ.get("CACHE_TTL", 500))


@extend_schema(
    parameters=[
        OpenApiParameter("city", OpenApiTypes.STR, OpenApiParameter.PATH),  # path variable was overridden
    ],
    request=None,
    responses=WeatherDataSerializer,
)
@api_view(['GET'])
@cache_page(CACHE_TTL)
def weather_by_city(request, city, format="json"):
    request_language = request.LANGUAGE_CODE.split('-')[0] or "en"
    owm_service = OpenWeatherMapService()

    city_data = owm_service.geocode(city, lang=request_language)
    weather_data = owm_service.weatherByLocation(city_data, lang=request_language)
    weather = WeatherData.create_from_openweathermap_data(city_data, weather_data)
    serializer = WeatherDataSerializer(weather, many=False)
    data = serializer.data

    data['wind_direction'] = _(data['wind_direction'])

    return Response(data)
