from django.utils import timezone
from django.db import transaction

from api.models import WaterData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_event_date,
)
from api.importing.mappings.waterdata_mapping import build_waterdata_payload


DEFAULT_HASH_FIELDS = [
    "eventID",
    "resourceName",
    "time",
    "locationID",
    "locality",
    "verbatimDepth",
    "waterTemperature",
    "conductivity",
    "salinity",
    "turbidity",
    "SS",
    "NH3_H",
    "NO2_H",
    "NO3_H",
    "PO4_P",
    "TBC",
    "vibrio",
    "COD",
    "MBAS",
    "TOC",
    "Lipid",
    "BOD5",
    "pH",
    "DO",
]


class WaterDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "event_date": validate_event_date,
        }

    def build_payload(self, record):
        return build_waterdata_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {}
        for f in self.hash_fields:
            hash_payload[f] = payload.get(f)
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            WaterData.objects.filter(dataID__in=keys).values_list("dataID", "data_hash")
        )

    def make_instance(self, payload):
        return WaterData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        # 更新時間統一在這裡做，service 不碰 model 細節
        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                WaterData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                WaterData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
