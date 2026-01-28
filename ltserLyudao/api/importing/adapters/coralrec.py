from django.utils import timezone
from django.db import transaction

from api.models import CoralData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_int,
    validate_event_date,
)

from api.importing.mappings.coralrec_mapping import build_coralrec_payload


DEFAULT_CORALREC_HASH_FIELDS = [
    "dataID",
    "eventID",
    "year",
    "month",
    "day",
    "time",
    "locationID",
    "verbatimLocality",
    "locality",
    "verbatimDepth",
    "decimalLatitude",
    "decimalLongitude",
    "replicate",
    "scientificName",
    "taxonRank",
    "family",
    "identificationRemarks",
    "measurementType",
    "measurementValue",
    "measurementUnit",
    "individualCount",
    "recordedBy",
    "identifiedBy",
    "samplingProtocol",
    "sampleSizeValue",
    "sampleSizeUnit",
]


class CoralRecDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_CORALREC_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "int": validate_int,
            "event_date": validate_event_date,
        }

    def build_payload(self, record):
        return build_coralrec_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {f: payload.get(f) for f in self.hash_fields}
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            CoralData.objects.filter(dataID__in=keys).values_list("dataID", "data_hash")
        )

    def make_instance(self, payload):
        return CoralData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                CoralData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                CoralData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
