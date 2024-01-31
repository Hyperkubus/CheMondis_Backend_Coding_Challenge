from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [
            'city_name',
            'city_longitude',
            'city_latitude',
            'current_temperature',
            'max_temperature',
            'min_temperature',
            'humidity',
            'pressure',
            'wind_speed',
            'wind_direction',
            'description'
        ]