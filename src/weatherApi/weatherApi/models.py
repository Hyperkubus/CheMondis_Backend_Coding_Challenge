from django.db import models


class WeatherData(models.Model):
    class WindDirection(models.TextChoices):
        north = 'North'
        east = 'East'
        south = 'South'
        west = 'West'

    city_name = models.CharField(max_length=180)  # should fit bangkoks full name
    city_longitude = models.FloatField()
    city_latitude = models.FloatField()
    current_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_temperature = models.FloatField()
    humidity = models.PositiveSmallIntegerField()
    pressure = models.PositiveSmallIntegerField()
    wind_speed = models.PositiveSmallIntegerField()
    wind_direction = models.CharField(default=WindDirection.north, choices=WindDirection.choices, max_length=5)
    description = models.TextField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    # In User class declaration
    @classmethod
    def create_from_openweathermap_data(cls, city, data):
        def degree_to_direction(deg):
            deg = deg % 360 # We should not rely on the input to be in a sensible range
            if 45 < deg < 135:
                return 'East'
            if deg < 225:
                return 'South'
            if deg < 315:
                return 'West'
            return 'North'

        return cls(
            city_name=city.name,
            city_longitude=city.lon,
            city_latitude=city.lat,
            current_temperature=data['main']['temp'],
            max_temperature=data['main']['temp_max'],
            min_temperature=data['main']['temp_min'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data['wind']['speed'],
            wind_direction=degree_to_direction(data['wind']['deg']),
            description=data['weather'][0]['description']
        )
