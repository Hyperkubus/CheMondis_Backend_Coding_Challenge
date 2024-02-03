from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('weather/<str:city>', views.weather_by_city)
]

urlpatterns = format_suffix_patterns(urlpatterns)