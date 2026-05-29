from django.utils import timezone
from django.db import transaction

from api.models import AquaticfaunaData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_int,
    validate_event_date,
)

from api.importing.mappings.aquaticfauna_mapping import build_aquaticfauna_payload


DEFAULT_AQUATICFAUNA_HASH_FIELDS = [
    "dataID",
    "eventID",
    "time",
    "season",
    "year",
    "month",
    "river",
    "locationID",
    "surveyObjectID",
    "surveyObject",
    "phylum",
    "phylum_c",
    "class_field",
    "class_c",
    "family",
    "family_c",
    "scientificName",
    "vernacularName",
    "taxonRank",
    "individualCount",
    "samplingProtocol",
    "abundance",
    "abundanceUnit",
    "informationWithheld",
]


class AquaticfaunaDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_AQUATICFAUNA_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "int": validate_int,
            "event_date": validate_event_date,
        }

    def build_payload(self, record):
        return build_aquaticfauna_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {}
        for f in self.hash_fields:
            hash_payload[f] = payload.get(f)
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return {
            data_id: {"id": pk, "data_hash": data_hash}
            for data_id, pk, data_hash in AquaticfaunaData.objects.filter(
                dataID__in=keys
            ).values_list("dataID", "id", "data_hash")
        }

    def make_instance(self, payload):
        return AquaticfaunaData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                AquaticfaunaData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                AquaticfaunaData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
