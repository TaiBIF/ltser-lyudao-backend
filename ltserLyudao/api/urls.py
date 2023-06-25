from django.urls import path
from .views import GetWeatherTimeRangeView, GetWeatherDetailView, GetSeaTemperatureTimeRangeView, GetSeaTemperatureDetailView, GetCoralDetailView

urlpatterns = [
    path('data/time-range/', GetWeatherTimeRangeView.as_view(), name='get_weather_time_range'),
    path('data/detail/', GetWeatherDetailView.as_view(), name='get_weather_detail'),
    path('data/sea-temperature/time-range/', GetSeaTemperatureTimeRangeView.as_view(),
         name='get_sea_temperature_time_range'),
    path('data/sea-temperature/detail/', GetSeaTemperatureDetailView.as_view(), name='get_sea_temperature_detail'),
    path('data/coral-rec/detail/', GetCoralDetailView.as_view(), name='get_coral_detail'),
]