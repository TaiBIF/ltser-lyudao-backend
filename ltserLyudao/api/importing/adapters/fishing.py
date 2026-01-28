from django.utils import timezone
from django.db import transaction

from api.models import FishingData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_boolean,
    validate_boolean_optional,
    validate_event_date,
)

from api.importing.mappings.fishing_mapping import build_fishing_payload


DEFAULT_FISHING_HASH_FIELDS = [
    "dataID",
    "eventID",
    "time",
    "locationID",
    "verbatimLocality",
    "is_local_villager",
    "purpose",
    "preferable_site",
    "catchment_individuals_per_month",
    "fishing_feq",
    "fishing_method",
    "bait",
    "fish_species",
    "feel_size_decrease",
]


class FishingDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_FISHING_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "boolean": validate_boolean,
            "event_date": validate_event_date,
        }

    def build_payload(self, record):
        return build_fishing_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {f: payload.get(f) for f in self.hash_fields}
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            FishingData.objects.filter(dataID__in=keys).values_list(
                "dataID", "data_hash"
            )
        )

    def make_instance(self, payload):
        return FishingData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                FishingData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                FishingData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
