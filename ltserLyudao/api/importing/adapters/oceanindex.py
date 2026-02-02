from django.utils import timezone
from django.db import transaction

from api.models import OceanSoundIndexData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_event_date,
    validate_int,
)

from api.importing.mappings.oceansound_mapping import build_ocean_sound_index_payload

DEFAULT_OCEAN_SOUND_INDEX_HASH_FIELDS = [
    "dataID",
    "eventID",
    "locationID",
    "time",
    "kHz0_24",
    "lower_200Hz",
    "Hz200_1500",
    "higher_1500Hz",
    "verbatimDepth",
]


class OceanSoundIndexDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_OCEAN_SOUND_INDEX_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "event_date": validate_event_date,
            "int": validate_int,
        }

    def build_payload(self, record):
        return build_ocean_sound_index_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {}
        for f in self.hash_fields:
            hash_payload[f] = payload.get(f)
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            OceanSoundIndexData.objects.filter(dataID__in=keys).values_list(
                "dataID", "data_hash"
            )
        )

    def make_instance(self, payload):
        return OceanSoundIndexData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                OceanSoundIndexData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                OceanSoundIndexData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
