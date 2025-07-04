from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import (
    WeatherTimeRangeSerializer,
    WeatherDetailSerializer,
    SeaTemperatureTimeRangeSerializer,
    SeaTemperatureDetailSerializer,
    CoralDetailSerializer,
    PlantDetailSerializer,
    BirdNetSoundDetailSerializer,
    FishDetailSerializer,
    ZoobenthosDataSerializer,
    WeatherChartSerializer,
    AquaticfaunaDataSerializer,
    MemorabiliaContentSerializer,
    LandUsageSerializer,
    OceanUsageSerializer,
    TemporalVariationSerializer,
    SocialInterviewSerializer,
    OccurrenceAPISerializer,
    DatasetSummarySerializer,
)
from rest_framework import status
from django.db.models import Sum, Avg, Q, Count, Func, F
from django.db.models import Value as V
from django.apps import apps
from django.core.paginator import Paginator
from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.http import FileResponse
from django.core.exceptions import ValidationError
import json
import io
import zipfile
import os
import csv
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from user.models import DownloadRecord, DownloadApply
from django.db.models import Sum
from rest_framework.fields import DateTimeField
from django.core.exceptions import ObjectDoesNotExist
from .conf.default_site_data import DEFAULT_SITE_DATA
from collections import defaultdict, OrderedDict
from django.core.cache import cache
import re
from api.utils.segisws_api import *
from user.models import SocialEconomyVisitors
from user.serializers import SocialEconomyVisitorsSerializer
import requests
from urllib.parse import urlparse, parse_qs


class SurveymapDropdownDataView(APIView):
    REVERSED_TABLE_MODELS = {
        CoralCommData: "coral-comm",
        WaterData: "water",
        WeatherData: "weather",
        HabitatData: "habitat",
        SeaTemperatureData: "sea-temperature",
        CoralData: "coral-rec",
        ZoobenthosData: "zoobenthos",
        PlantData: "plant",
        BirdNetSoundData: "bird-net-sound",
        FishData: "fish-div",
        FishingData: "fishing",
        OceanSoundIndexData: "ocean-sound-index",
        BioSoundData: "bio-sound",
        TerreSoundIndexData: "terre-sound-index",
        AquaticfaunaData: "aquaticfauna",
        StreamData: "stream",
        OtolithData: "otolith",
        CoralDivData: "coral-div",
        CoralBleachData: "coral-bleach",
    }

    def get_data_from_model(self, model):
        site_data = {site: data.copy() for site, data in DEFAULT_SITE_DATA.items()}

        model_name = self.REVERSED_TABLE_MODELS.get(model, None)
        if model_name is None:
            return []

        # 額外模型的的處理
        if hasattr(model, "locationID"):
            sites = model.objects.values_list("locationID", flat=True).distinct()
        else:
            return []

        for site in sites:
            if site not in site_data:
                site_data[site] = {"site": site, "years": []}

            if hasattr(model, "year"):
                year_values = (
                    model.objects.filter(locationID=site)
                    .values_list("year", flat=True)
                    .distinct()
                )
            else:
                year_values = (
                    model.objects.filter(locationID=site)
                    .annotate(year=models.functions.ExtractYear("time"))
                    .values_list("year", flat=True)
                    .distinct()
                )

            for year in year_values:
                year_str = str(year)
                existing_year = next(
                    (y for y in site_data[site]["years"] if y["year"] == year_str), None
                )

                if existing_year:
                    if model_name not in existing_year["items"]:
                        existing_year["items"].append(model_name)
                else:
                    site_data[site]["years"].append(
                        {"year": year_str, "items": [model_name]}
                    )
        return list(site_data.values())

    def get(self, request, *args, **kwargs):

        cached_data = cache.get("surveymap_options")

        if cached_data:  # 如果 Redis 中已有資料直接回傳
            return Response(json.loads(cached_data), status=status.HTTP_200_OK)

        all_data = []
        models = [
            WeatherData,
            CoralData,
            PlantData,
            FishData,
            ZoobenthosData,
            WaterData,
            HabitatData,
            CoralCommData,
            OceanSoundIndexData,
            AquaticfaunaData,
            StreamData,
            OtolithData,
            CoralDivData,
            CoralBleachData,
            TerreSoundIndexData,
            BirdNetSoundData,
            BioSoundData,
            SeaTemperatureData,
        ]

        all_data = defaultdict(lambda: {"site": None, "years": []})

        for model in models:
            model_data = self.get_data_from_model(model)
            for site_info in model_data:
                site = site_info["site"]
                existing_site = all_data[site]
                existing_site["site"] = site

                for year_info in site_info["years"]:
                    year = year_info["year"]
                    existing_year = next(
                        (y for y in existing_site["years"] if y["year"] == year), None
                    )
                    if existing_year:
                        for item in year_info["items"]:
                            if item not in existing_year["items"]:
                                existing_year["items"].append(item)
                    else:
                        existing_site["years"].append(year_info)

        # 將結果用 redis cache 起來，保存期限為 7 天
        cache.set(
            "surveymap_options", json.dumps(list(all_data.values())), timeout=604800
        )

        return Response(list(all_data.values()), status=status.HTTP_200_OK)


class FormatDateTime(Func):
    function = "to_char"
    template = "%(function)s(%(expressions)s, '%s')"

    def __init__(self, field_name):
        super().__init__(
            F(field_name), template=self.template % "YYYY-MM-DD HH24:MI:SS"
        )


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data, total_records):
        total_pages = (total_records // self.page_size) + (
            1 if total_records % self.page_size else 0
        )
        return Response(
            {
                "currentPage": self.page_number,
                "recordsPerPage": self.page_size,
                "totalPages": total_pages,
                "totalRecords": total_records,
                "records": data,
            }
        )


SEA_TEMPERATURE_TABLES = [
    "SeaTemperatureCK2023",
    "SeaTemperatureDBS2023",
    "SeaTemperatureGG2023",
    "SeaTemperatureGW2023",
    "SeaTemperatureNL2023",
    "SeaTemperatureSL2023",
    "SeaTemperatureWQG2023",
    "SeaTemperatureYZH2023",
    "SeaTemperatureZP2023",
]
BIRD_NET_SOUND_TABLES = [
    "BirdNetSoundBS2023",
    "BirdNetSoundGST2023",
    "BirdNetSoundLH2023",
    "BirdNetSoundYZH2023",
]
BIO_SOUND_TABLES = [
    "BioSoundBS2023",
    "BioSoundGST2023",
    "BioSoundLH2023",
    "BioSoundYZH2023",
]
TERRE_SOUND_TABLES = [
    "TerreSoundIndexBS2023",
    "TerreSoundIndexGST2023",
    "TerreSoundIndexLH2023",
    "TerreSoundIndexYZH2023",
]


class GetWeatherTimeRangeView(APIView):
    def get(self, request):
        location_id = request.GET.get("locationID")

        weather_data = WeatherData.objects.filter(locationID=location_id)

        if not weather_data.exists():
            return Response(
                {"error": "Weather data not found."}, status=status.HTTP_404_NOT_FOUND
            )

        min_event_date = weather_data.earliest("eventDate").eventDate
        max_event_date = weather_data.latest("eventDate").eventDate

        serializer = WeatherTimeRangeSerializer(weather_data, many=True)

        response_data = {
            "site": location_id,
            "start": min_event_date.strftime("%Y-%m-%d"),
            "end": max_event_date.strftime("%Y-%m-%d"),
        }

        return Response(response_data)


class GetWeatherDetailView(APIView):
    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year value."}, status=400)

        weather_data = WeatherData.objects.filter(
            locationID=location_id, time__year=year
        )

        if not weather_data.exists():
            return Response({"error": "Weather data not found."}, status=404)

        annual_precipitation_sum = weather_data.aggregate(
            precipitation_sum=Sum("precipitation")
        )["precipitation_sum"]
        annual_rounded_precipitation = (
            round(annual_precipitation_sum, 4)
            if annual_precipitation_sum is not None
            else None
        )
        seasonal_data = []

        for season in [(1, 3), (4, 6), (7, 9), (10, 12)]:
            season_data = weather_data.filter(time__month__range=season)
            season_precipitation_sum = season_data.aggregate(
                precipitation_sum=Sum("precipitation")
            )["precipitation_sum"]
            season_rounded_precipitation = (
                round(season_precipitation_sum, 4)
                if season_precipitation_sum is not None
                else None
            )
            season_temperature_avg = season_data.aggregate(
                temperature_avg=Avg("airTemperature")
            )["temperature_avg"]
            season_rounded_temperature = (
                round(season_temperature_avg, 2)
                if season_temperature_avg is not None
                else None
            )
            seasonal_data.append(
                {
                    "season": f"{season[0]}-{season[1]}",
                    "airTemperature": season_rounded_temperature,
                    "precipitation": season_rounded_precipitation,
                }
            )

        response_data = {
            "site": location_id,
            "year": str(year),
            "annual": {
                "airTemperature": None,  # 暫時先設為None
                "precipitation": annual_rounded_precipitation,
            },
            "seasonal": seasonal_data,
        }

        # 計算全年平均溫度
        annual_temperature_avg = weather_data.aggregate(
            temperature_avg=Avg("airTemperature")
        )["temperature_avg"]
        response_data["annual"]["airTemperature"] = (
            round(annual_temperature_avg, 2)
            if annual_temperature_avg is not None
            else None
        )

        # 計算每個季節的平均溫度
        for season in response_data["seasonal"]:
            season_data = weather_data.filter(
                time__month__range=(
                    int(season["season"].split("-")[0]),
                    int(season["season"].split("-")[1]),
                )
            )
            season_temperature_avg = season_data.aggregate(
                temperature_avg=Avg("airTemperature")
            )["temperature_avg"]
            season["airTemperature"] = (
                round(season_temperature_avg, 2)
                if season_temperature_avg is not None
                else None
            )

        serializer = WeatherDetailSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSeaTemperatureTimeRangeView(APIView):
    MODELS = {
        "CK": "SeaTemperatureCK2023",
        "DBS": "SeaTemperatureDBS2023",
        "GG": "SeaTemperatureGG2023",
        "GW": "SeaTemperatureGW2023",
        "NL": "SeaTemperatureNL2023",
        "SL": "SeaTemperatureSL2023",
        "WQG": "SeaTemperatureWQG2023",
        "YZH": "SeaTemperatureYZH2023",
        "ZP": "SeaTemperatureZP2023",
    }

    def get(self, request):
        location_id = request.GET.get("locationID")
        model_name = self.MODELS.get(location_id)

        if not model_name:
            return Response(
                {"error": "Invalid locationID."}, status=status.HTTP_404_NOT_FOUND
            )

        ModelClass = apps.get_model("api", model_name)

        try:
            min_event_date = ModelClass.objects.earliest("time").time
            max_event_date = ModelClass.objects.latest("time").time
        except ModelClass.DoesNotExist:
            return Response(
                {"error": "No data for this location."},
                status=status.HTTP_404_NOT_FOUND,
            )

        response_data = {
            "site": location_id,
            "start": min_event_date.strftime("%Y-%m-%d"),
            "end": max_event_date.strftime("%Y-%m-%d"),
        }

        serializer = SeaTemperatureTimeRangeSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(response_data)


class GetSeaTemperatureDetailView(APIView):

    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year value."}, status=400)

        sea_temperature_data = SeaTemperatureData.objects.filter(
            locationID=location_id, time__year=year
        )

        if not sea_temperature_data.exists():
            return Response({"error": "Sea temperature data not found."}, status=404)

        seasonal_data = []
        for season in [(1, 3), (4, 6), (7, 9), (10, 12)]:
            season_data = sea_temperature_data.filter(time__month__range=season)
            season_temperature_avg = season_data.aggregate(
                temperature_avg=Avg("seaTemperature")
            )["temperature_avg"]
            season_rounded_temperature = (
                round(season_temperature_avg, 2)
                if season_temperature_avg is not None
                else None
            )
            seasonal_data.append(
                {
                    "season": f"{season[0]}-{season[1]}",
                    "seaTemperature": season_rounded_temperature,
                }
            )

        response_data = {
            "site": location_id,
            "year": str(year),
            "annual": {
                "seaTemperature": None,
            },
            "seasonal": seasonal_data,
        }

        annual_temperature_avg = sea_temperature_data.aggregate(
            temperature_avg=Avg("seaTemperature")
        )["temperature_avg"]
        response_data["annual"]["seaTemperature"] = (
            round(annual_temperature_avg, 2)
            if annual_temperature_avg is not None
            else None
        )

        serializer = SeaTemperatureDetailSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCoralDetailView(APIView):
    def get(self, request):
        location_id = request.query_params.get("locationID")
        year = request.query_params.get("year")

        if not CoralData.objects.filter(locationID=location_id).exists():
            return Response({"error": "Invalid locationID."}, status=400)

        total_count = (
            CoralData.objects.filter(locationID=location_id, year=year).aggregate(
                total_count=Sum("individualCount")
            )["total_count"]
            or 0
        )

        serializer = CoralDetailSerializer(
            data={
                "site": location_id,
                "year": year,
                "count": total_count,
            }
        )

        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class GetPlantDetailView(APIView):
    def get(self, request):
        location_id = request.query_params.get("locationID")
        year = request.query_params.get("year")

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year value."}, status=400)

        if not PlantData.objects.filter(locationID=location_id).exists():
            return Response({"error": "Invalid locationID."}, status=400)

        seasons = ["1-3", "4-6", "7-9", "10-12"]
        seasonal_counts = []
        for season in seasons:
            distinct_names_count = (
                PlantData.objects.filter(
                    locationID=location_id,
                    time__year=year,
                    time__month__in=range(
                        int(season.split("-")[0]), int(season.split("-")[1]) + 1
                    ),
                )
                .values("scientificName")
                .distinct()
                .count()
            )
            seasonal_counts.append({"season": season, "count": distinct_names_count})

        serializer = PlantDetailSerializer(seasonal_counts, many=True)

        data = {
            "site": location_id,
            "year": year,
            "seasonal": serializer.data,
        }

        return Response(data)


class GetBirdNetSoundDetailView(APIView):

    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year value."}, status=400)

        bird_net_sound_data = BirdNetSoundData.objects.filter(time__year=year)
        if not bird_net_sound_data.exists():
            return Response({"error": "Bird Net Sound data not found."}, status=404)

        data = []
        for i in range(0, 12, 3):
            season = f"{i + 1}-{i + 3}"
            count = (
                bird_net_sound_data.filter(time__month__range=(i + 1, i + 3))
                .values("scientificName")
                .distinct()
                .count()
            )

            data.append(
                {
                    "season": season,
                    "count": count,
                }
            )

        result = {
            "site": location_id,
            "year": year,
            "seasonal": data,
        }

        serializer = BirdNetSoundDetailSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetFishDetailView(APIView):

    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        try:
            year = int(year)
        except ValueError:
            return Response(
                {"error": "Invalid year value."}, status=status.HTTP_400_BAD_REQUEST
            )

        fish_data = FishData.objects.filter(locationID=location_id, time__year=year)

        if not fish_data.exists():
            return Response(
                {"error": "Fish data not found."}, status=status.HTTP_404_NOT_FOUND
            )

        seasonal_data = []
        for season, months in [
            ("1-3", [1, 2, 3]),
            ("4-6", [4, 5, 6]),
            ("7-9", [7, 8, 9]),
            ("10-12", [10, 11, 12]),
        ]:
            count = (
                fish_data.filter(time__month__in=months)
                .values("scientificName")
                .distinct()
                .count()
            )
            seasonal_data.append({"season": season, "count": count})

        data = {
            "site": location_id,
            "year": year,
            "seasonal": seasonal_data,
        }

        serializer = FishDetailSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetZoobenthosDetailView(APIView):
    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        if not ZoobenthosData.objects.filter(locationID=location_id).exists():
            return Response({"error": "Invalid locationID."}, status=400)

        queryset = ZoobenthosData.objects.filter(locationID=location_id, year=year)
        seasons = ["1-3", "4-6", "7-9", "10-12"]
        seasonal_counts = []

        for season in seasons:
            start_month, end_month = map(int, season.split("-"))
            season_query = queryset.filter(month__range=[start_month, end_month])
            species_count = season_query.values("scientificName").distinct().count()
            seasonal_counts.append({"season": season, "count": species_count})

        response_data = {
            "site": location_id,
            "year": year,
            "seasonal": seasonal_counts,
        }

        serializer = ZoobenthosDataSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class GetAquaticfaunaDetailView(APIView):
    def get(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        if not AquaticfaunaData.objects.filter(locationID=location_id).exists():
            return Response({"error": "Invalid locationID."}, status=400)

        queryset = AquaticfaunaData.objects.filter(locationID=location_id, year=year)
        seasons = ["1-3", "4-6", "7-9", "10-12"]
        seasonal_counts = []

        for season in seasons:
            start_month, end_month = map(int, season.split("-"))
            season_query = queryset.filter(month__range=[start_month, end_month])
            species_count = season_query.values("scientificName").distinct().count()
            seasonal_counts.append({"season": season, "count": species_count})

        response_data = {
            "site": location_id,
            "year": year,
            "seasonal": seasonal_counts,
        }

        serializer = AquaticfaunaDataSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class GetTableFieldsView(APIView):
    TABLE_MODELS = {
        "coral-comm": CoralCommData,
        "water": WaterData,
        "weather": WeatherData,
        "habitat": HabitatData,
        "sea-temperature": BaseSeaTemperatureData,
        "coral-rec": CoralData,
        "zoobenthos": ZoobenthosData,
        "plant": PlantData,
        "bird-net-sound": BaseBirdNetSoundData,
        "fish-div": FishData,
        "fishing": FishingData,
        "ocean-sound-index": OceanSoundIndexData,
        "bio-sound": BaseBioSoundData,
        "terre-sound-index": BaseTerreSoundIndexData,
        "aquaticfauna": AquaticfaunaData,
        "stream": StreamData,
        "otolith": OtolithData,
        "coral-div": CoralDivData,
        "coral-bleach": CoralBleachData,
    }

    FIELD_INFO_MODELS = {
        "coral-comm": CoralCommDataField,
        "water": WaterDataField,
        "weather": WeatherDataField,
        "habitat": HabitatDataField,
        "sea-temperature": SeaTemperatureDataField,
        "coral-rec": CoralDataField,
        "zoobenthos": ZoobenthosDataField,
        "plant": PlantDataField,
        "bird-net-sound": BirdNetSoundDataField,
        "fish-div": FishDataField,
        "fishing": FishingDataField,
        "ocean-sound-index": OceanSoundIndexDataField,
        "bio-sound": BioSoundDataField,
        "terre-sound-index": TerreSoundIndexDataField,
        "aquaticfauna": AquaticfaunaDataField,
        "stream": StreamDataField,
        "otolith": OtolithDataField,
        "coral-div": CoralDivDataField,
        "coral-bleach": CoralBleachDataField,
    }

    def get(self, request, table):
        language = request.headers.get("Ltser-User-Language", "zh-tw")
        model = self.TABLE_MODELS.get(table)

        if model is None:
            return Response(
                {"error": f'Table "{table}" not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        field_info_model = self.FIELD_INFO_MODELS.get(table)
        if field_info_model is None:
            return Response(
                {"error": f'Field information model for table "{table}" not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        fields = []

        for field_info in field_info_model.objects.all():
            title = (
                field_info.title_zh_tw if language == "zh-tw" else field_info.title_en
            )
            content = (
                field_info.content_zh_tw
                if language == "zh-tw"
                else field_info.content_en
            )

            fields.append(
                {
                    "id": field_info.field_name,
                    "type": self.get_field_type(field_info.field_type),
                    "title": title,
                    "content": content,
                    "show": field_info.show,
                }
            )

        return Response(fields)

    def get_field_type(self, field_type):
        if field_type is None:
            return "unknown"
        field_type = field_type.lower()  # convert to lowercase
        if field_type in ["integerfield", "autofield", "floatfield", "decimalfield"]:
            return "number"
        elif field_type in ["textfield", "charfield"]:
            return "text"
        elif field_type in ["datefield", "datetimefield"]:
            return "date"
        else:
            return "unknown"


class GetDataRawAPIView(APIView):
    TABLE_MODELS = {
        "coral-comm": "CoralCommData",
        "habitat": "HabitatData",
        "water": "WaterData",
        "weather": "WeatherData",
        "sea-temperature": "SeaTemperatureData",
        "coral-rec": "CoralData",
        "zoobenthos": "ZoobenthosData",
        "plant": "PlantData",
        "bird-net-sound": "BirdNetSoundData",
        "fish-div": "FishData",
        "fishing": "FishingData",
        "ocean-sound-index": "OceanSoundIndexData",
        "bio-sound": "BioSoundData",
        "terre-sound-index": "TerreSoundIndexData",
        "aquaticfauna": "AquaticfaunaData",
        "stream": "StreamData",
        "otolith": "OtolithData",
        "coral-div": "CoralDivData",
        "coral-bleach": "CoralBleachData",
    }

    @staticmethod
    def get_field_names_without_id(model):
        return [field.name for field in model._meta.fields if field.name != "id"]

    def get(self, request, table, *args, **kwargs):
        model_name = self.TABLE_MODELS.get(table)
        if not model_name:
            return Response({"error": "Table not found"}, status=404)
        all_data = []
        query_params = request.query_params.dict()
        page_size = query_params.pop("page_size", 10)
        page = query_params.pop("page", 1)
        if "cursor" in query_params:
            query_params.pop("cursor")  # 刪除不需要的參數

        # 額外處理日期、日期時間的查詢，避免進入迴圈造成重複或錯誤
        time_param = query_params.pop("time", None)
        end_time_param = query_params.pop("end_time", None)

        model = apps.get_model("api", model_name)
        query = Q()
        for key, value in query_params.items():
            if isinstance(model._meta.get_field(key), models.CharField):
                query &= Q(**{f"{key}__icontains": value})
            else:
                query &= Q(**{f"{key}": value})

        field_type = model._meta.get_field("time")
        if isinstance(
            field_type, models.DateTimeField
        ):  # 如果是 DateTimeField 欄位，使用__date過濾器來根據日期查詢
            if time_param and end_time_param:
                # 查詢 time_param 和 end_time_param 之間的結果
                query &= Q(**{f"time__date__range": [time_param, end_time_param]})
            elif time_param:
                # 查詢 time_param 以後的所有結果
                query &= Q(**{f"time__date__gte": time_param})
            elif end_time_param:
                # 查詢 end_time_param 以前的所有結果
                query &= Q(**{f"time__date__lte": end_time_param})
        elif isinstance(field_type, models.DateField):
            if time_param and end_time_param:
                # 查詢 time_param 和 end_time_param 之間的結果
                query &= Q(**{f"time__range": [time_param, end_time_param]})
            elif time_param:
                # 查詢 time_param 以後的所有結果
                query &= Q(**{f"time__gte": time_param})
            elif end_time_param:
                # 查詢 end_time_param 以前的所有結果
                query &= Q(**{f"time__lte": end_time_param})

        # 在查詢之前就先限制回傳的資料筆數
        offset = (int(page) - 1) * int(page_size)
        limit = int(page_size)
        fields_without_id = GetDataRawAPIView.get_field_names_without_id(model)
        filtered_data = model.objects.filter(query).values(*fields_without_id)[
            offset : offset + limit
        ]
        total_records = model.objects.filter(query).count()

        if (
            table == "water"
            or table == "habitat"
            or table == "coral-comm"
            or table == "fish-div"
            or table == "aquaticfauna"
            or table == "stream"
        ):
            for record in filtered_data:
                if "time" in record and record["time"]:
                    formatted_time = record["time"].strftime("%Y-%m-%d")
                    record["time"] = formatted_time
        else:
            for record in filtered_data:
                if "time" in record and record["time"]:
                    formatted_time = record["time"].strftime("%Y-%m-%d %H:%M:%S")
                    record["time"] = formatted_time

        all_data.extend(list(filtered_data))
        paginator = CustomPageNumberPagination()
        if page_size:
            paginator.page_size = min(int(page_size), paginator.max_page_size)
        paginator.page_number = int(page)
        return paginator.get_paginated_response(filtered_data, total_records)


class GetWeatherChartAPIView(APIView):
    def get(self, request):
        start_date = make_aware(datetime(2023, 3, 8))
        end_date = start_date + timedelta(days=1)

        # Filter for the entire range of the target day
        weather_data = WeatherData.objects.filter(time__range=(start_date, end_date))
        serializer = WeatherChartSerializer(weather_data, many=True)
        return Response(serializer.data)


class DownloadHomePageAPIView(APIView):
    def get_filter(self, item, location_id, year):
        filter_dict = {"locationID": location_id, "time__year": year}
        return filter_dict

    def save_download_record(self, user, filename):
        download_record = DownloadRecord(filename=filename, user=user)
        download_record.save()

    def save_download_apply(self, request, filename):
        email = request.data.get("email")
        role = request.data.get("role")
        content = request.data.get("content")

        if email and role and content:
            download_apply = DownloadApply(
                email=email, role=role, content=content, filename=filename
            )
            download_apply.save()
        else:
            raise ValidationError("Missing required fields.")

    def _download_logic(self, request):
        location_id = request.GET.get("locationID")
        year = request.GET.get("year")

        sites_json_path = os.path.join(os.path.dirname(__file__), "sites.json")
        with open(sites_json_path) as f:
            sites = json.load(f)

        for site in sites:
            if site["site"] == location_id:
                for site_year in site["years"]:
                    if site_year["year"] == year:
                        items = site_year["items"]
                        break
                else:
                    continue
                break
        else:
            return {
                "error": Response(
                    {"detail": "Location ID not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            }

        if not items:
            return {
                "error": Response(
                    {"detail": "No data for this year"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            }

        item_to_model = {
            "sea-temperature": f"SeaTemperature{location_id}2023",
            "coral-rec": "CoralData",
            "fish-div": "FishData",
            "plant": "PlantData",
            "weather": "WeatherData",
            "zoobenthos": "ZoobenthosData",
            "bird-net-sound": f"BirdNetSound{location_id}2023",
            "aquaticfauna": "AquaticfaunaData",
        }

        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, "w", zipfile.ZIP_DEFLATED) as zipf:
            for item in items:
                model_name = item_to_model.get(item)
                if model_name is None:
                    continue
                model = apps.get_model("api", model_name)
                csv_file = f"{item}-{location_id}-{year}.csv"

                with open(csv_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([field.name for field in model._meta.fields])
                    for instance in model.objects.filter(
                        **self.get_filter(item, location_id, year)
                    ):
                        writer.writerow(
                            [
                                getattr(instance, field.name)
                                for field in model._meta.fields
                            ]
                        )

                zipf.write(csv_file)
                os.remove(csv_file)

        zip_io.seek(0)
        filename = f"{location_id}_{year}.zip"
        response = FileResponse(zip_io, as_attachment=True, filename=filename)
        return {"response": response, "filename": filename}

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Unauthorized GET request."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        download_data = self._download_logic(request)
        if "error" in download_data:
            return download_data["error"]

        self.save_download_record(request.user, download_data["filename"])

        return download_data["response"]

    def post(self, request):
        download_data = self._download_logic(request)
        if "error" in download_data:
            return download_data["error"]

        try:
            self.save_download_apply(request, download_data["filename"])
            if request.user.is_authenticated:
                self.save_download_record(request.user, download_data["filename"])
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return download_data["response"]


class GetTableSitesAPIView(APIView):
    table_models = {
        "coral-comm": CoralCommData,
        "habitat": HabitatData,
        "water": WaterData,
        "weather": WeatherData,
        "plant": PlantData,
        "fish-div": FishData,
        "zoobenthos": ZoobenthosData,
        "coral-rec": CoralData,
        "ocean-sound-index": OceanSoundIndexData,
        "fishing": FishingData,
        "aquaticfauna": AquaticfaunaData,
        "stream": StreamData,
        "terre-sound-index": TerreSoundIndexData,
        "bird-net-sound": BirdNetSoundData,
        "bio-sound": BioSoundData,
        "sea-temperature": SeaTemperatureData,
        "otolith": OtolithData,
    }

    def get(self, request, table):
        language = request.headers.get("Ltser-User-Language", "zh-tw")
        model = self.table_models.get(table)

        if model:
            sites = model.objects.values_list("locationID", flat=True).distinct()
            sites_info = []
            for site_id in sites:
                try:
                    location = LocationTableInfo.objects.get(location_id=site_id)
                    site_name = (
                        location.name_zh if language == "zh-tw" else location.name_en
                    )
                    sites_info.append({"id": site_id, "title": site_name})
                except ObjectDoesNotExist:
                    continue
            return Response({"sites": sites_info})

        else:
            return Response(
                {"error": "Invalid table parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetTableSeriesAPIView(APIView):
    TABLE_MODELS = {
        "water": {
            "model": "WaterData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "waterTemperature",
                    "title": {"zh-tw": "水溫", "en": "waterTemperature"},
                },
                {"name": "salinity", "title": {"zh-tw": "鹽度", "en": "salinity"}},
                {
                    "name": "conductivity",
                    "title": {"zh-tw": "導電度", "en": "conductivity"},
                },
                {"name": "turbidity", "title": {"zh-tw": "濁度", "en": "turbidity"}},
                {"name": "SS", "title": {"zh-tw": "氣溫", "懸浮固體": "SS"}},
                {"name": "TBC", "title": {"zh-tw": "總菌落數", "en": "TBC"}},
                {"name": "vibrio", "title": {"zh-tw": "弧菌", "en": "vibrio"}},
            ],
        },
        "weather": {
            "model": "WeatherData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {"name": "windSpeed", "title": {"zh-tw": "風速", "en": "windSpeed"}},
                {
                    "name": "windDirection",
                    "title": {"zh-tw": "風向", "en": "windDirection"},
                },
                {
                    "name": "precipitation",
                    "title": {"zh-tw": "雨量", "en": "precipitation"},
                },
                {
                    "name": "airTemperature",
                    "title": {"zh-tw": "氣溫", "en": "airTemperature"},
                },
            ],
        },
        "sea-temperature": {
            "model": "SeaTemperatureData",
            # 'models': {
            #     'CK': 'SeaTemperatureCK2023',
            #     'DBS': 'SeaTemperatureDBS2023',
            #     'GG': 'SeaTemperatureGG2023',
            #     'GW': 'SeaTemperatureGW2023',
            #     'NL': 'SeaTemperatureNL2023',
            #     'SL': 'SeaTemperatureSL2023',
            #     'WQG': 'SeaTemperatureWQG2023',
            #     'YZH': 'SeaTemperatureYZH2023',
            #     'ZP': 'SeaTemperatureZP2023',
            # },
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "seaTemperature",
                    "title": {"zh-tw": "海溫", "en": "seaTemperature"},
                },
            ],
        },
        "terre-sound-index": {
            # 'models': {
            #     'BS': 'TerreSoundIndexBS2023',
            #     'GST': 'TerreSoundIndexGST2023',
            #     'LH': 'TerreSoundIndexLH2023',
            #     'YZH': 'TerreSoundIndexYZH2023',
            # },
            "model": "TerreSoundIndexData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {"name": "ACI", "title": {"zh-tw": "聲音複雜度指數", "en": "ACI"}},
                {"name": "ADI", "title": {"zh-tw": "聲音多樣性指數", "en": "ADI"}},
                {"name": "BI", "title": {"zh-tw": "生物聲音指數", "en": "BI"}},
                {"name": "NDSI", "title": {"zh-tw": "標準化聲景指數", "en": "NDSI"}},
            ],
        },
        "coral-rec": {
            "model": "CoralData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "珊瑚礁入添數量",
                        "en": "Number of Coral Reef Juvenile",
                    },
                },
            ],
        },
        "coral-comm": {
            "model": "CoralCommData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "sampleSizeValue",
                    "title": {
                        "zh-tw": "珊瑚礁群聚調查數量",
                        "en": "Number of Coral Reef Aggregation Surveys",
                    },
                },
            ],
        },
        "fish-div": {
            "model": "FishData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {"zh-tw": "魚種數", "en": "Number of Fish Species"},
                },
            ],
        },
        "plant": {
            "model": "PlantData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "陸域植物種類數",
                        "en": "Number of Terrestrial Plant Species",
                    },
                },
            ],
        },
        "zoobenthos": {
            "model": "ZoobenthosData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "底棲動物種類數",
                        "en": "Number of Benthic Fauna Species",
                    },
                },
            ],
        },
        "bird-net-sound": {
            # 'models': {
            #     'BS': 'BirdNetSoundBS2023',
            #     'GST': 'BirdNetSoundGST2023',
            #     'LH': 'BirdNetSoundLH2023',
            #     'YZH': 'BirdNetSoundYZH2023',
            # },
            "model": "BirdNetSoundData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "鳥種數(鳥音)",
                        "en": "Number of Bird Species (Sound Identification)",
                    },
                },
            ],
        },
        "bio-sound": {
            # 'models':{
            #     'BS': 'BioSoundBS2023',
            #     'GST': 'BioSoundGST2023',
            #     'LH': 'BioSoundLH2023',
            #     'YZH': 'BioSoundYZH2023',
            # },
            "model": "BioSoundData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "生物物種數",
                        "en": "Number of biological species",
                    },
                },
            ],
        },
        "ocean-sound-index": {
            "model": "OceanSoundIndexData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "lower_200Hz",
                    "title": {"zh-tw": "聲壓值強度：低頻", "en": "0_200Hz"},
                },
                {
                    "name": "Hz200_1500",
                    "title": {"zh-tw": "聲壓值強度：中頻 ", "en": "200_1500Hz"},
                },
                {
                    "name": "higher_1500Hz",
                    "title": {"zh-tw": "聲壓值強度：高頻", "en": "higher_1500Hz"},
                },
            ],
        },
        "habitat": {
            "model": "HabitatData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                # {'name': 'locationID', 'title': {'zh-tw': '地點', 'en': 'locationID'}},
                {"name": "score", "title": {"zh-tw": "分數", "en": "score"}},
            ],
        },
        "aquaticfauna": {
            "model": "AquaticfaunaData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "scientificName",
                    "title": {
                        "zh-tw": "生物物種數",
                        "en": "Number of biological species",
                    },
                },
            ],
        },
        "stream": {
            "model": "StreamData",
            "fields": [
                {"name": "time", "title": {"zh-tw": "time", "en": "time"}},
                {
                    "name": "waterTemperature",
                    "title": {"zh-tw": "水溫", "en": "waterTemperature"},
                },
                {"name": "pH", "title": {"zh-tw": "酸鹼度", "en": "pH"}},
                {"name": "DO", "title": {"zh-tw": "溶氧", "en": "DO"}},
                {
                    "name": "conductivity",
                    "title": {"zh-tw": "導電度", "en": "conductivity"},
                },
                {"name": "salinity", "title": {"zh-tw": "鹽度", "en": "salinity"}},
                {"name": "SS", "title": {"zh-tw": "懸浮固體", "en": "SS"}},
                {
                    "name": "RPI_Score",
                    "title": {"zh-tw": "RPI污染程度計算分數", "en": "RPI_Score"},
                },
            ],
        },
    }

    def get(self, request, table):
        language = request.headers.get("Ltser-User-Language", "zh-tw")
        location_id = request.query_params.get("locationID")
        depth = request.query_params.get("depth")

        if not location_id:
            return Response(
                {"error": "No locationID provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        table_config = self.TABLE_MODELS.get(table)

        if not table_config:
            return Response(
                {"error": "Invalid table parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model_name = table_config.get("model")

        if not model_name:
            return Response(
                {"error": "Invalid locationID parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model = apps.get_model("api", model_name)
        field_configurations = table_config["fields"]
        field_names = [
            field["name"] for field in field_configurations if isinstance(field, dict)
        ]

        queryset = model.objects.filter(locationID=location_id)
        try:
            if table == "habitat":
                data = (
                    queryset.values("time")
                    .annotate(score=Sum("score"))
                    .order_by("time")
                )
            elif table in ["water", "weather", "sea-temperature", "stream"]:
                data = queryset.order_by("time").values(*field_names)
            elif table == "ocean-sound-index":
                data = (
                    queryset.filter(verbatimDepth=depth)
                    .order_by("time")
                    .values(*field_names)
                )
            elif table == "coral-comm":
                data = (
                    queryset.values("time", "Benthic_group")
                    .annotate(total_cover=Sum("coverInPercentage"))
                    .order_by("time", "Benthic_group")
                )
            else:
                data = (
                    queryset.order_by("time")
                    .values("time")
                    .annotate(scientificName=Count("scientificName", distinct=True))
                )
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 確保資料不為空
        if not data:
            return Response(
                {"error": f"No data found for locationID {location_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        formatted_data = []
        if table != "coral-comm":
            date_format = (
                "%Y-%m-%d %H:%M:%S"
                if table
                not in ["water", "fish-div", "coral-comm", "aquaticfauna", "stream"]
                else "%Y-%m-%d"
            )
            for record in data:
                formatted_record = {
                    field.get("title", {}).get(language, field["name"]): record.get(
                        field["name"], ""
                    )
                    for field in field_configurations
                    if isinstance(field, dict)
                }

                if "time" in record:
                    formatted_record["time"] = record["time"].strftime(date_format)
                formatted_data.append(formatted_record)
        else:
            grouped_data = defaultdict(dict)
            total_cover_num = defaultdict(float)  # 存儲每個時間點的 total_cover 總和

            for record in data:
                time = record["time"]
                benthic_group = record["Benthic_group"]
                total_cover = record["total_cover"]

                if time in total_cover_num:
                    total_cover_num[time] += total_cover
                else:
                    total_cover_num[time] = total_cover

                grouped_data[time][benthic_group] = total_cover

            # 標準化數據為百分比
            formatted_data = []
            for time, values in grouped_data.items():
                # 取出該時間點的 total_cover 總和
                total_cover = total_cover_num[time]
                # 計算百分比
                percentage_values = {
                    group: (cover / total_cover) * 100  # 將數據轉換為百分比
                    for group, cover in values.items()
                }

                formatted_entry = {"time": time, "coverage": percentage_values}
                formatted_data.append(formatted_entry)

        return Response(formatted_data)


class DownloadRawAPIView(APIView):
    TABLE_MODELS = {
        "coral-comm": ["CoralCommData"],
        "habitat": ["HabitatData"],
        "water": ["WaterData"],
        "weather": ["WeatherData"],
        "sea-temperature": SEA_TEMPERATURE_TABLES,
        "coral-rec": ["CoralData"],
        "zoobenthos": ["ZoobenthosData"],
        "plant": ["PlantData"],
        "bird-net-sound": BIRD_NET_SOUND_TABLES,
        "fish-div": ["FishData"],
        "fishing": ["FishingData"],
        "bio-sound": BIO_SOUND_TABLES,
        "aquaticfauna": ["AquaticfaunaData"],
        "stream": ["StreamData"],
        "terre-sound-index": TERRE_SOUND_TABLES,
    }

    def save_download_record(self, user, filename):
        download_record = DownloadRecord(filename=filename, user=user)
        download_record.save()

    def save_download_apply(self, request, filename):
        email = request.data.get("email")
        role = request.data.get("role")
        content = request.data.get("content")

        if email and role and content:
            download_apply = DownloadApply(
                email=email, role=role, content=content, filename=filename
            )
            download_apply.save()
        else:
            raise ValidationError("Missing required fields.")

    @staticmethod
    def get_field_names_without_id(model):
        return [field.name for field in model._meta.fields if field.name != "id"]

    def _download_logic(self, request, table, *args, **kwargs):
        species = "species" in request.path_info
        model_names = self.TABLE_MODELS.get(table)
        if not model_names:
            return {"error": {"message": "Table not found", "status": 404}}
        all_data = []
        for model_name in model_names:
            model = apps.get_model("api", model_name)
            query_params = request.query_params.dict()
            page_number = int(query_params.pop("page", 1))
            query = Q()
            for key, value in query_params.items():
                field_type = model._meta.get_field(key)
                if key == "time" and isinstance(
                    field_type, models.DateTimeField
                ):  # 查詢參數中的日期
                    query &= Q(
                        **{f"{key}__date": value}
                    )  # 使用__date過濾器來根據日期查詢
                elif key == "time" and isinstance(field_type, models.DateField):
                    query &= Q(**{f"{key}": value})  # 直接使用日期值進行查詢
                elif isinstance(model._meta.get_field(key), models.CharField):
                    query &= Q(**{f"{key}__icontains": value})
                else:
                    query &= Q(**{f"{key}": value})
            fields_without_id = GetDataRawAPIView.get_field_names_without_id(model)
            filtered_data = model.objects.filter(query).values(*fields_without_id)

            if (
                table == "water"
                or table == "habitat"
                or table == "coral-comm"
                or table == "fish-div"
                or table == "aquaticfauna"
                or table == "stream"
            ):
                for record in filtered_data:
                    if "time" in record and record["time"]:
                        formatted_time = record["time"].strftime("%Y-%m-%d")
                        record["time"] = formatted_time
            else:
                for record in filtered_data:
                    if "time" in record and record["time"]:
                        formatted_time = record["time"].strftime("%Y-%m-%d %H:%M:%S")
                        record["time"] = formatted_time

            species_fields = ["scientificName", "vernacularName", "taxonRank", "family"]

            if species:
                distinct_data = set()
                for record in filtered_data:
                    new_record = {
                        k: v for k, v in record.items() if k in species_fields
                    }
                    distinct_data.add(tuple(new_record.items()))

                filtered_data = [dict(t) for t in distinct_data]

            all_data.extend(list(filtered_data))

        zip_io = io.BytesIO()

        with zipfile.ZipFile(zip_io, "w", zipfile.ZIP_DEFLATED) as zipf:
            csv_filename = f"{table}.csv"

            # 使用io.StringIO作為暫存的CSV檔
            with io.StringIO() as csv_io:
                writer = csv.DictWriter(csv_io, fieldnames=all_data[0].keys())
                writer.writeheader()
                for row in all_data:
                    writer.writerow(row)

                # 將StringIO內的CSV內容寫入ZIP檔
                zipf.writestr(csv_filename, csv_io.getvalue())
        zip_io.seek(0)
        filename = f"{table}.zip"
        response = FileResponse(zip_io, as_attachment=True, filename=filename)
        return {"response": response, "filename": filename}

    def get(self, request, table, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Unauthorized GET request."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        download_data = self._download_logic(request, table, *args, **kwargs)
        if "error" in download_data:
            return Response(
                download_data["error"]["message"],
                status=download_data["error"]["status"],
            )

        self.save_download_record(request.user, download_data["filename"])

        return download_data["response"]

    def post(self, request, table, *args, **kwargs):
        download_data = self._download_logic(request, table, *args, **kwargs)
        if "error" in download_data:
            return Response(
                download_data["error"]["message"],
                status=download_data["error"]["status"],
            )

        try:
            self.save_download_apply(request, download_data["filename"])
            if request.user.is_authenticated:
                self.save_download_record(request.user, download_data["filename"])
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return download_data["response"]


class GetAllDetailsAPIView(APIView):
    def get(self, request):

        response_data = {
            "weather": {},
            "seaTemperature": {},
            "plant": {},
            "birdNetSound": {},
            "fishDiv": {},
            "zoobenthos": {},
            "aquaticfauna": {},
        }

        weather_view = GetWeatherDetailView()
        weather_response = weather_view.get(request)
        if weather_response.status_code == status.HTTP_200_OK:
            response_data["weather"] = weather_response.data

        sea_temperature_view = GetSeaTemperatureDetailView()
        sea_temperature_response = sea_temperature_view.get(request)
        if sea_temperature_response.status_code == status.HTTP_200_OK:
            response_data["seaTemperature"] = sea_temperature_response.data

        plant_view = GetPlantDetailView()
        plant_response = plant_view.get(request)
        if plant_response.status_code == status.HTTP_200_OK:
            response_data["plant"] = plant_response.data

        birdNetSound_view = GetBirdNetSoundDetailView()
        birdNetSound_response = birdNetSound_view.get(request)
        if birdNetSound_response.status_code == status.HTTP_200_OK:
            response_data["birdNetSound"] = birdNetSound_response.data

        fishDiv_view = GetFishDetailView()
        fishDiv_response = fishDiv_view.get(request)
        if fishDiv_response.status_code == status.HTTP_200_OK:
            response_data["fishDiv"] = fishDiv_response.data

        zoobenthos_view = GetZoobenthosDetailView()
        zoobenthos_response = zoobenthos_view.get(request)
        if zoobenthos_response.status_code == status.HTTP_200_OK:
            response_data["zoobenthos"] = zoobenthos_response.data

        aquaticfauna_view = GetAquaticfaunaDetailView()
        aquaticfauna_response = aquaticfauna_view.get(request)
        if aquaticfauna_response.status_code == status.HTTP_200_OK:
            response_data["aquaticfauna"] = aquaticfauna_response.data

        return Response(response_data, status=status.HTTP_200_OK)


class MemorabiliaContentAPIView(APIView):
    def get(self, request):
        data = MemorabiliaContent.objects.all()
        serializer = MemorabiliaContentSerializer(data, many=True)

        return Response(serializer.data)


class LandUsageAPIView(APIView):
    def get(self, request):
        data = LandUsage.objects.all().order_by("id")
        serializer = LandUsageSerializer(data, many=True)

        return Response(serializer.data)


class OceanUsageAPIView(APIView):
    def get(self, request):
        data = OceanUsage.objects.all().order_by("id")
        serializer = OceanUsageSerializer(data, many=True)

        return Response(serializer.data)


class TemporalVariationAPIView(APIView):
    def get(self, request):
        data = TemporalVariation.objects.all().order_by("id")
        serializer = TemporalVariationSerializer(data, many=True)

        return Response(serializer.data)


class SocialInterviewAPIView(APIView):
    def get(self, request):
        query_params = request.query_params.dict()
        page = query_params.pop("page", 1)
        participant_type_params = query_params.pop("participantType", None)
        cap_issue_type_params = query_params.pop("capIssueType", None)
        local_issue_type_params = query_params.pop("localIssueType", None)
        keyword_params = query_params.pop("keyword", None)
        content_params = query_params.pop("content", None)
        id_pramas = query_params.pop("id", None)

        filter_conditions = Q()

        if participant_type_params:
            filter_conditions &= Q(participant_type=participant_type_params)

        if cap_issue_type_params:
            if isinstance(cap_issue_type_params, str):
                issue_type_list = cap_issue_type_params.split(",")
            elif isinstance(cap_issue_type_params, list):
                issue_type_list = cap_issue_type_params
            else:
                issue_type_list = []

            cap_issue_conditions = Q()
            for issue in issue_type_list:
                cap_issue_conditions &= Q(CAP_issue__contains=issue)

            filter_conditions &= cap_issue_conditions

        if local_issue_type_params:
            if isinstance(local_issue_type_params, str):
                issue_type_list = local_issue_type_params.split(",")
            elif isinstance(local_issue_type_params, list):
                issue_type_list = local_issue_type_params
            else:
                issue_type_list = []

            local_issue_conditions = Q()
            for issue in issue_type_list:
                local_issue_conditions &= Q(local_issue__contains=issue)

            filter_conditions &= local_issue_conditions

        if keyword_params:
            filter_conditions &= Q(tag__contains=keyword_params)

        if content_params:
            filter_conditions &= Q(text__contains=content_params)

        if id_pramas:
            filter_conditions &= Q(id=id_pramas)

        # 議題列表資料
        paginator = CustomPageNumberPagination()
        data_queryset = SocialInterview.objects.filter(filter_conditions).order_by("id")
        total_records_queryset = data_queryset.count()
        paginator.page_number = int(page)
        paginated_data = paginator.paginate_queryset(data_queryset, request)
        serializer = SocialInterviewSerializer(paginated_data, many=True)
        paginated_response = paginator.get_paginated_response(
            serializer.data, total_records_queryset
        )

        # 受訪對象下拉選單資料
        participant_types = SocialInterview.objects.values_list(
            "participant_type", flat=True
        ).distinct()
        participant_types_result = [
            {"id": idx + 1, "title": participant_type}
            for idx, participant_type in enumerate(participant_types)
        ]

        # CAP議題分類勾選資料
        cap_issues = SocialInterview.objects.values_list(
            "CAP_issue", flat=True
        ).distinct()
        cap_issues_split = []
        for cap_issue in cap_issues:
            cap_issues_split.extend(
                # cap issue 前面有編號時，去除編號以及空格，只保留文字；沒有編號時去除空格
                [
                    (
                        item.split(".", 1)[1].strip()
                        if "." in item.strip()
                        else item.strip()
                    )
                    for item in cap_issue.split(";")
                ]
            )

        cap_issues_cleaned = sorted(set(cap_issues_split), key=lambda x: x.strip())
        cap_issues_result = []
        for idx, issue in enumerate(cap_issues_cleaned, start=1):
            matched_issue = SocialInterviewCapIssues.objects.filter(
                cap_issue=issue
            ).first()
            cap_issues_result.append(
                {
                    "id": idx,
                    "title": (
                        matched_issue.cap_issue_mandarin if matched_issue else None
                    ),
                    "value": issue,
                }
            )

        cap_issues_result = sorted(
            cap_issues_result,
            key=lambda x: (
                int(re.match(r"(\d+)", x["title"]).group())
                if re.match(r"(\d+)", x["title"])
                else float("inf")
            ),
        )

        # 在地議題分類勾選資料
        local_issues = SocialInterview.objects.values_list(
            "local_issue", flat=True
        ).distinct()
        local_issues_split = []
        for local_issue in local_issues:
            local_issues_split.extend([item.strip() for item in local_issue.split(";")])

        local_issues_cleaned = sorted(set(local_issues_split), key=lambda x: x.strip())
        local_issues_result = [
            {"id": idx + 1, "title": issue}
            for idx, issue in enumerate(local_issues_cleaned)
        ]

        response_data = {
            "data": paginated_response.data["records"],
            "participant_types_result": participant_types_result,
            "cap_issues_result": cap_issues_result,
            "local_issues_result": local_issues_result,
            "pagination": {
                "currentPage": paginated_response.data["currentPage"],
                "recordsPerPage": paginated_response.data["recordsPerPage"],
                "totalPages": paginated_response.data["totalPages"],
                "totalRecords": paginated_response.data["totalRecords"],
            },
        }

        return Response(response_data)


class SocialEconomyPopulationAPIView(APIView):
    def get(self, request):
        cached_data = cache.get("social_economy_population")

        if cached_data:  # 如果 Redis 中已有資料直接回傳
            return Response(json.loads(cached_data), status=status.HTTP_200_OK)

        # 村里-人口統計
        latest_time = get_latest_time_list("village", query_type="summary")
        village_population = get_population_data(
            "village", latest_time, query_type="summary"
        )

        # 村里-人口指標
        latest_time = get_latest_time_list("village", query_type="index")
        village_index = get_population_data("village", latest_time, query_type="index")

        # 村里-人口消長
        latest_time = get_latest_time_list("village", query_type="dynamics")
        village_dynamics = get_population_data(
            "village", latest_time, query_type="dynamics"
        )

        # 鄉鎮-人口統計
        latest_time = get_latest_time_list("town", query_type="summary")
        town_population = get_population_data("town", latest_time, query_type="summary")

        # 鄉鎮-人口指標
        latest_time = get_latest_time_list("town", query_type="index")
        town_index = get_population_data("town", latest_time, query_type="index")

        # 鄉鎮-人口消長
        latest_time = get_latest_time_list("town", query_type="dynamics")
        town_dynamics = get_population_data("town", latest_time, query_type="dynamics")

        # 鄉鎮-人口結構
        latest_time = get_latest_time_list("town", query_type="pyramid")
        town_pyramid = get_population_data("town", latest_time, query_type="pyramid")

        sorted_population_data = {}
        sorted_pyramid_data = {}

        for entry in village_population:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['V_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "H_CNT": int(round(entry["H_CNT"])),
                    "P_CNT": int(round(entry["P_CNT"])),
                }
            )

        for entry in village_index:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['V_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "M_F_RAT": round(entry["M_F_RAT"], 2),
                    "DEPENDENCY_RAT": round(entry["DEPENDENCY_RAT"], 2),
                    "A65_A0A14_RAT": round(entry["A65_A0A14_RAT"], 2),
                }
            )

        for entry in village_dynamics:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['V_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "NATURE_INC_CNT": int(round(entry["NATURE_INC_CNT"])),
                    "SOCIAL_INC_CNT": int(round(entry["SOCIAL_INC_CNT"])),
                }
            )

        for entry in town_population:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['TOWN_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "H_CNT": int(round(entry["H_CNT"])),
                    "P_CNT": int(round(entry["P_CNT"])),
                }
            )

        for entry in town_index:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['TOWN_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "M_F_RAT": round(entry["M_F_RAT"], 2),
                    "DEPENDENCY_RAT": round(entry["DEPENDENCY_RAT"], 2),
                    "A65_A0A14_RAT": round(entry["A65_A0A14_RAT"], 2),
                }
            )

        for entry in town_dynamics:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            key = f"{year},{entry['TOWN_ID']}"
            if key not in sorted_population_data:
                sorted_population_data[key] = {}
            sorted_population_data[key].update(
                {
                    "NATURE_INC_CNT": int(round(entry["NATURE_INC_CNT"])),
                    "SOCIAL_INC_CNT": int(round(entry["SOCIAL_INC_CNT"])),
                }
            )

        sorted_population_data = dict(
            sorted(
                sorted_population_data.items(),
                key=lambda item: int(item[0].split(",")[0].replace("Y", "")),
            )
        )

        for entry in town_pyramid:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            if year not in sorted_pyramid_data:
                sorted_pyramid_data[year] = {}
            for key, value in entry.items():
                if isinstance(value, (int, float)):
                    sorted_pyramid_data[year][key] = int(round(value))
                else:
                    sorted_pyramid_data[year][key] = value

        sorted_pyramid_data = dict(
            sorted(
                sorted_pyramid_data.items(),
                key=lambda item: int(item[0].replace("Y", "")),
            )
        )

        response = {
            "population": sorted_population_data,
            "pyramid": sorted_pyramid_data,
        }

        if len(sorted_population_data) > 0 and len(sorted_pyramid_data) > 0:
            # 將結果用 redis cache 起來，保存期限為 7 天
            cache.set("social_economy_population", json.dumps(response), timeout=604800)

        return Response(response)


class SocialEconomyIndustryAPIView(APIView):
    def get(self, request):
        # 鄉鎮-觀光人次統計，直接跟資料庫取資料
        visitors = SocialEconomyVisitors.objects.all().order_by("year")
        serializer = SocialEconomyVisitorsSerializer(visitors, many=True)
        sorted_visitor_data = serializer.data

        cached_data = cache.get("social_economy_industry")

        if cached_data:  # 如果 Redis 中已有資料直接回傳
            cached_data = json.loads(cached_data)
            cached_data["visitor"] = (
                sorted_visitor_data  # 觀光人次每次都取最新的資料回傳
            )
            return Response(cached_data, status=status.HTTP_200_OK)

        sorted_industry_data = {}
        sorted_fishing_data = {}
        sorted_livestock_data = {}

        # 鄉鎮-工商家數統計
        latest_time = get_latest_time_list("town", query_type="industry")
        industry_summary = get_industry_data(latest_time, query_type="industry")

        # 鄉鎮-漁戶統計
        latest_time = get_latest_time_list("town", query_type="fishing")
        fishing_summary = get_industry_data(latest_time, query_type="fishing")

        # 鄉鎮-牲畜統計
        latest_time = get_latest_time_list("town", query_type="livestock")
        livestock_summary = get_industry_data(latest_time, query_type="livestock")

        for entry in industry_summary:
            year = entry["INFO_TIME"].split("Y")[0] + "Y"
            if year not in sorted_industry_data:
                sorted_industry_data[year] = {}
            for key, value in entry.items():
                if isinstance(value, (int, float)):
                    sorted_industry_data[year][key] = int(round(value))
                else:
                    sorted_industry_data[year][key] = value

        sorted_industry_data = dict(
            sorted(
                sorted_industry_data.items(),
                key=lambda item: int(item[0].replace("Y", "")),
            )
        )

        for entry in fishing_summary:
            key = entry["INFO_TIME"]
            if key not in sorted_fishing_data:
                sorted_fishing_data[key] = {}
            sorted_fishing_data[key].update(
                {
                    "COL_1": int(round(entry["COL_1"])),
                    "COL_8": int(round(entry["COL_8"])),
                }
            )

        sorted_fishing_data = dict(
            sorted(
                sorted_fishing_data.items(),
                key=lambda item: int(item[0].replace("Y", "")),
            )
        )

        for entry in livestock_summary:
            key = entry["INFO_TIME"]
            if key not in sorted_livestock_data:
                sorted_livestock_data[key] = {}
            sorted_livestock_data[key].update(
                {
                    "COL_1": int(round(entry["COL_1"])),
                    "COL_3": int(round(entry["COL_3"])),
                    "COL_4": int(round(entry["COL_4"])),
                    "COL_5": int(round(entry["COL_5"])),
                    "COL_7": int(round(entry["COL_7"])),
                }
            )

        sorted_livestock_data = dict(
            sorted(
                sorted_livestock_data.items(),
                key=lambda item: int(item[0].replace("Y", "")),
            )
        )

        response = {
            "industry": sorted_industry_data,
            "fishing": sorted_fishing_data,
            "livestock": sorted_livestock_data,
            "visitor": sorted_visitor_data,
        }

        if (
            len(sorted_industry_data) > 0
            and len(sorted_fishing_data) > 0
            and len(sorted_livestock_data) > 0
        ):
            # 將結果用 redis cache 起來，保存期限為 7 天
            cache.set("social_economy_industry", json.dumps(response), timeout=604800)
        return Response(response)


class APIPagination(LimitOffsetPagination):
    default_limit = 10  # 預設回傳 10 筆
    max_limit = 50  # 最多回傳 50 筆


class OccurrenceAPIView(APIView):
    pagination_class = APIPagination

    TABLE_MODELS = {
        "coral-div": CoralDivData,
        "coral-bleach": CoralBleachData,
        "coral-rec": CoralData,
        "zoobenthos": ZoobenthosData,
        "plant": PlantData,
        "bird-net-sound": BirdNetSoundData,
        "bio-sound": BioSoundData,
        "fish-div": FishData,
        "aquaticfauna": AquaticfaunaData,
        "otolith": OtolithData,
    }

    def get(self, request):
        paginator = self.pagination_class()
        dataset_name = request.query_params.get("datasetName")

        if not dataset_name:
            return Response({"detail": "datasetName is required"}, status=400)

        if dataset_name not in self.TABLE_MODELS:
            return Response({"detail": "datasetName is not valid"}, status=400)

        model = self.TABLE_MODELS[dataset_name]

        # 動態生成欄位
        fields = ["scientificName"]
        if hasattr(model, "decimalLongitude") and hasattr(model, "decimalLatitude"):
            fields += ["decimalLongitude", "decimalLatitude"]

        queryset = model.objects.values(*fields).annotate(
            occurrenceID=F("dataID"),
            datasetName=V(dataset_name),
            license=V("CC-BY 4.0"),
        )

        paginator = self.pagination_class()
        pagination_data = paginator.paginate_queryset(queryset, request, view=self)

        # 使用序列化器進行資料轉換
        serializer = OccurrenceAPISerializer(pagination_data, many=True)

        return paginator.get_paginated_response(serializer.data)


class DatasetSummaryAPIView(APIView):
    pagination_class = APIPagination

    def get(self, request):
        paginator = self.pagination_class()

        data_summary = DatasetSummary.objects.all()

        pagination_data = paginator.paginate_queryset(data_summary, request, view=self)
        serializer = DatasetSummarySerializer(pagination_data, many=True)

        return paginator.get_paginated_response(serializer.data)


class GetThirdPartyTableFieldsView(APIView):

    FIELD_INFO_MODELS = {"tbia": TBIADataField}

    def get(self, request, table):
        language = request.headers.get("Ltser-User-Language", "zh-tw")

        field_info_model = self.FIELD_INFO_MODELS.get(table)
        if field_info_model is None:
            return Response(
                {"error": f'Field information model for table "{table}" not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        fields = []

        for field_info in field_info_model.objects.all():
            title = (
                field_info.title_zh_tw if language == "zh-tw" else field_info.title_en
            )
            content = (
                field_info.content_zh_tw
                if language == "zh-tw"
                else field_info.content_en
            )

            fields.append(
                {
                    "id": field_info.field_name,
                    "type": self.get_field_type(field_info.field_type),
                    "title": title,
                    "content": content,
                    "show": field_info.show,
                }
            )

        return Response(fields)

    def get_field_type(self, field_type):
        if field_type is None:
            return "unknown"
        field_type = field_type.lower()  # convert to lowercase
        if field_type in ["integerfield", "autofield", "floatfield", "decimalfield"]:
            return "number"
        elif field_type in ["textfield", "charfield"]:
            return "text"
        elif field_type in ["datefield", "datetimefield"]:
            return "date"
        else:
            return "unknown"


class GetThirdPartyDataRawAPIView(APIView):
    API_CONFIG = {
        "tbia": {
            "url": "https://tbiadata.tw/api/v1/occurrence?circle=121.488,22.661,10",
            "required_fileds": [
                "scientificName",
                "common_name_c",
                "alternative_name_c",
                "synonyms",
                "misapplied",
                "sourceScientificName",
                "sourceVernacularName",
                "originalScientificName",
                "bioGroup",
                "taxonRank",
                "sensitiveCategory",
                "rightsHolder",
                "taxonID",
                "eventDate",
                "county",
                "municipality",
                "locality",
                "organismQuantity",
                "organismQuantityType",
                "recordedBy",
                "verbatimSRS",
                "verbatimLongitude",
                "verbatimLatitude",
                "verbatimCoordinateSystem",
                "coordinateUncertaintyInMeters",
                "dataGeneralizations",
                "coordinatePrecision",
                "basisOfRecord",
                "datasetName",
                "resourceContacts",
                "datasetLicense",
            ],
        }
    }

    def get(self, request, table, *args, **kwargs):
        api_url = self.API_CONFIG.get(table).get("url")
        query_params = request.query_params.dict()
        print(query_params)
        if "page_size" in query_params:
            query_params["limit"] = query_params.pop("page_size")

        if "eventDate" in query_params and "eventEndDate" in query_params:
            query_params["eventDate"] = (
                f"{query_params['eventDate']},{query_params['eventEndDate']}"
            )
            query_params.pop("eventEndDate", None)

        if not api_url:
            return Response({"error": "Table not found"}, status=404)

        response = requests.get(api_url, params=query_params)
        if response.status_code == 200:
            data = response.json()
            total_records = data.get("meta", {}).get("total", "")
            next_url = data.get("links", {}).get("next", "")

            if next_url:
                parsed_url = urlparse(next_url)
                query_params = parse_qs(parsed_url.query)
                cursor = query_params.get("cursor", [None])[0]
            else:
                cursor = None

            records = data.get("data", [])
            filtered_records = [
                {
                    key: record[key]
                    for key in self.API_CONFIG.get(table).get("required_fileds")
                    if key in record
                }
                for record in records
            ]
            return Response(
                {
                    "currentPage": 1,
                    "recordsPerPage": 20,
                    "totalPages": 2,
                    "nextCursor": cursor,
                    "totalRecords": total_records,
                    "records": filtered_records,
                }
            )
        else:
            return Response(
                {"error": "API response error"}, status=response.status_code
            )
