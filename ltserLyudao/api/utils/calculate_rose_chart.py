from django.db.models import Value as V
from django.db.models import (
    Case,
    When,
    CharField,
)


def convert_to_direction_bin(field_name):
    """將風向、流向欄位中的數值轉成方位，共分成八個方位"""
    return Case(
        When(**{f"{field_name}__gte": 337.5}, then=V("N")),
        When(**{f"{field_name}__lt": 22.5}, then=V("N")),
        When(
            **{f"{field_name}__gte": 22.5, f"{field_name}__lt": 67.5},
            then=V("NE"),
        ),
        When(
            **{f"{field_name}__gte": 67.5, f"{field_name}__lt": 112.5},
            then=V("E"),
        ),
        When(
            **{f"{field_name}__gte": 112.5, f"{field_name}__lt": 157.5},
            then=V("SE"),
        ),
        When(
            **{f"{field_name}__gte": 157.5, f"{field_name}__lt": 202.5},
            then=V("S"),
        ),
        When(
            **{f"{field_name}__gte": 202.5, f"{field_name}__lt": 247.5},
            then=V("SW"),
        ),
        When(
            **{f"{field_name}__gte": 247.5, f"{field_name}__lt": 292.5},
            then=V("W"),
        ),
        When(
            **{f"{field_name}__gte": 292.5, f"{field_name}__lt": 337.5},
            then=V("NW"),
        ),
        default=V("Unknown"),
        output_field=CharField(),
    )


def pick_bin_key(range):
    """取區間中的第一個值出來做當做排序的 key"""
    try:
        return float(range.split("-")[0])
    except:
        return float("inf")
