from rest_framework import serializers
from .models import WeatherData
from django.utils.translation import gettext
from rest_framework.validators import UniqueValidator
from drf_yasg.openapi import Schema, TYPE_STRING
from drf_yasg.utils import swagger_serializer_method
from drf_yasg import openapi

class WeatherTimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'

class WeatherDetailSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()
    annual = serializers.DictField(child=serializers.FloatField())

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        airTemperature = serializers.FloatField(allow_null=True)
        precipitation = serializers.FloatField(allow_null=True)

    seasonal = SeasonalSerializer(many=True)


class SeaTemperatureTimeRangeSerializer(serializers.Serializer):
    site = serializers.CharField(max_length=255)
    start = serializers.DateField()
    end = serializers.DateField()

class SeaTemperatureDetailSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()
    annual = serializers.DictField(child=serializers.FloatField())

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        seaTemperature = serializers.FloatField(allow_null=True)

    seasonal = SeasonalSerializer(many=True)


class CoralDetailSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()
    count = serializers.IntegerField()

class PlantDetailSerializer(serializers.Serializer):
    season = serializers.CharField()
    count = serializers.IntegerField()

class BirdNetSoundDetailSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        count = serializers.IntegerField()

    seasonal = SeasonalSerializer(many=True)