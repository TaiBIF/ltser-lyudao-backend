from django.utils import timezone
from django.db import transaction

from api.models import SeaTemperatureData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_event_datetime,
)

from api.importing.mappings.seatemperature_mapping import build_sea_temperature_payload


DEFAULT_SEA_TEMPERATURE_HASH_FIELDS = [
    "dataID",
    "eventID",
    "resourceName",
    "locationID",
    "verbatimDepth",
    "fieldNumber",
    "time",
    "seaTemperature",
]


class SeaTemperatureDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_SEA_TEMPERATURE_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "event_datetime": validate_event_datetime,
        }

    def build_payload(self, record):
        return build_sea_temperature_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {}
        for f in self.hash_fields:
            hash_payload[f] = payload.get(f)
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            SeaTemperatureData.objects.filter(dataID__in=keys).values_list(
                "dataID", "data_hash"
            )
        )

    def make_instance(self, payload):
        return SeaTemperatureData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                SeaTemperatureData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                SeaTemperatureData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
