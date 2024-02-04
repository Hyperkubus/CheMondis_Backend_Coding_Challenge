import asyncio
import os

from django.views.decorators.cache import cache_page

from adrf.decorators import api_view
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
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
#@cache_page(CACHE_TTL)
async def weather_by_city(request, city, format="json"):
    request_language = request.LANGUAGE_CODE.split('-')[0] or "en"
    owm_service = OpenWeatherMapService()
    city_data_task = asyncio.create_task(owm_service.geocode(city, lang=request_language))
    city_data = await city_data_task
    weather_data_task = asyncio.create_task(owm_service.weatherByLocation(city_data, lang=request_language))
    weather_data = await weather_data_task
    weather = WeatherData.create_from_openweathermap_data(city_data, weather_data)
    serializer = WeatherDataSerializer(weather, many=False)
    data = serializer.data

    data['wind_direction'] = _(data['wind_direction'])

    return Response(data)
