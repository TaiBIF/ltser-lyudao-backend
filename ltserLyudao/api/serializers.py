from rest_framework import serializers
from .models import WeatherData, MemorabiliaContent, LandUsage, OceanUsage, TemporalVariation, SocialInterview
from django.utils.translation import gettext
from rest_framework.validators import UniqueValidator
from drf_yasg.openapi import Schema, TYPE_STRING
from drf_yasg.utils import swagger_serializer_method
from drf_yasg import openapi
from django.apps import apps
from django.db import models

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

class WeatherChartSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = WeatherData
        fields = ('time', 'windSpeed', 'windDirection', 'precipitation', 'airTemperature')

    def get_time(self, obj):
        return obj.eventDate.strftime('%Y/%m/%d %H:%M:%S')


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

class FishDetailSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        count = serializers.IntegerField()

    seasonal = SeasonalSerializer(many=True)

class ZoobenthosDataSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        count = serializers.IntegerField()

    seasonal = SeasonalSerializer(many=True)

class AquaticfaunaDataSerializer(serializers.Serializer):
    site = serializers.CharField()
    year = serializers.CharField()

    class SeasonalSerializer(serializers.Serializer):
        season = serializers.CharField()
        count = serializers.IntegerField()

    seasonal = SeasonalSerializer(many=True)

class MemorabiliaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemorabiliaContent
        fields = ['image', 'description']

class LandUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandUsage
        fields = ['image', 'description', 'content']

class OceanUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OceanUsage
        fields = ['image', 'description', 'content']

class TemporalVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalVariation
        fields = ['image', 'description', 'content']

class SocialInterviewSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()

    class Meta:
        model = SocialInterview
        fields = ['id', 'dataID', 'time', 'text', 'CAP_issue', 'local_issue', 'tag', 'participant_type']

    def get_tag(self, obj):
        # 將 tag 欄位轉換為列表
        return [tag for tag in obj.tag.split(';') if tag.strip()] if obj.tag else []



