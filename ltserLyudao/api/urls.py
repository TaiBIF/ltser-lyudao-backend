from django.urls import path
from .views import GetWeatherTimeRangeView, GetWeatherDetailView

urlpatterns = [
    path('data/time-range/', GetWeatherTimeRangeView.as_view(), name='get_weather_time_range'),
    path('data/detail/', GetWeatherDetailView.as_view(), name='get_weather_detail_view')
]