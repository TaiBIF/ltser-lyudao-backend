from django.urls import path
from .views import GetWeatherTimeRangeView, GetWeatherDetailView, GetSeaTemperatureTimeRangeView, \
    GetSeaTemperatureDetailView, GetCoralDetailView, GetPlantDetailView, GetBirdNetSoundDetailView, \
    GetFishDetailView, GetZoobenthosDetailView, GetTableFieldsView, GetDataListView

urlpatterns = [
    path('data/time-range/', GetWeatherTimeRangeView.as_view(), name='get_weather_time_range'),
    path('data/weather/detail/', GetWeatherDetailView.as_view(), name='get_weather_detail'),
    path('data/sea-temperature/time-range/', GetSeaTemperatureTimeRangeView.as_view(),
         name='get_sea_temperature_time_range'),
    path('data/sea-temperature/detail/', GetSeaTemperatureDetailView.as_view(), name='get_sea_temperature_detail'),
    path('data/coral-rec/detail/', GetCoralDetailView.as_view(), name='get_coral_detail'),
    path('data/plant/detail/', GetPlantDetailView.as_view(), name='get_plant_detail'),
    path('data/bird-net-sound/detail/', GetBirdNetSoundDetailView.as_view(), name='get_bird_net_sound_detail'),
    path('data/fish-div/detail/', GetFishDetailView.as_view(), name='get_fish_detail'),
    path('data/zoobenthos/detail/', GetZoobenthosDetailView.as_view(), name='get_zoobenthos_detail'),
    path('data/<str:table>/fields/', GetTableFieldsView.as_view(), name='get_table_fields'),
    path('data/<str:table>/',GetDataListView.as_view(), name='get_data_list')
]