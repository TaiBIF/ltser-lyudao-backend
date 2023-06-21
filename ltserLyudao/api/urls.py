from django.urls import path
from .views import GetWeatherTimeRangeView, GetWeatherDetailView

urlpatterns = [
    path('getWeatherTimeRange/', GetWeatherTimeRangeView.as_view(), name='get_weather_time_range'),
    path('getWeatherDetail/', GetWeatherDetailView.as_view(), name='get_weather_detail_view')
]