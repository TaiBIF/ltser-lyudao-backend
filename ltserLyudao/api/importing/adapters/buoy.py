from django.utils import timezone
from django.db import transaction

from api.models import BuoyData
from api.utils.hashing import compute_data_hash
from api.utils.validators import (
    validate_required,
    validate_decimal,
    validate_int,
    validate_event_date,
)

from api.importing.mappings.buoy_mapping import build_buoy_payload


DEFAULT_BUOY_HASH_FIELDS = [
    "dataID",
    "eventID",
    "eventDate",
    "eventTime",
    "locationID",
    "underwater_par",
    "terrestrial_par",
    "exo_temperature",
    "sp_cond",
    "salinity",
    "ph",
    "odo_sat",
    "odo",
    "aquadopp_temperature",
    "corrected_wind_direction",
    "corrected_wind_speed",
    "air_temperature",
    "relative_humidity",
    "barometric_pressure",
    "precipitation_intensity",
    "precipitation_total",
    "wmo_average_wind_direction",
    "wmo_average_wind_speed",
    "latitude",
    "longitude",
    "vel_e_cell_1",
    "vel_n_cell_1",
    "vel_u_cell_1",
    "current_speed_1",
    "current_direction_1",
    "vel_e_cell_2",
    "vel_n_cell_2",
    "vel_u_cell_2",
    "current_speed_2",
    "current_direction_2",
    "vel_e_cell_3",
    "vel_n_cell_3",
    "vel_u_cell_3",
    "current_speed_3",
    "current_direction_3",
    "vel_e_cell_4",
    "vel_n_cell_4",
    "vel_u_cell_4",
    "current_speed_4",
    "current_direction_4",
    "vel_e_cell_5",
    "vel_n_cell_5",
    "vel_u_cell_5",
    "current_speed_5",
    "current_direction_5",
    "vel_e_cell_6",
    "vel_n_cell_6",
    "vel_u_cell_6",
    "current_speed_6",
    "current_direction_6",
    "vel_e_cell_7",
    "vel_n_cell_7",
    "vel_u_cell_7",
    "current_speed_7",
    "current_direction_7",
    "vel_e_cell_8",
    "vel_n_cell_8",
    "vel_u_cell_8",
    "current_speed_8",
    "current_direction_8",
    "vel_e_cell_9",
    "vel_n_cell_9",
    "vel_u_cell_9",
    "current_speed_9",
    "current_direction_9",
    "vel_e_cell_10",
    "vel_n_cell_10",
    "vel_u_cell_10",
    "current_speed_10",
    "current_direction_10",
    "time",
]


class BuoyDataAdapter:
    key_field = "dataID"

    def __init__(self, hash_fields=None):
        self.hash_fields = hash_fields or list(DEFAULT_BUOY_HASH_FIELDS)
        self.validators = {
            "required": validate_required,
            "decimal": validate_decimal,
            "event_date": validate_event_date,
        }

    def build_payload(self, record):
        return build_buoy_payload(record, self.validators)

    def compute_hash(self, payload):
        hash_payload = {f: payload.get(f) for f in self.hash_fields}
        return compute_data_hash(hash_payload)

    def fetch_existing_hash_map(self, keys):
        if not keys:
            return {}
        return dict(
            BuoyData.objects.filter(dataID__in=keys).values_list("dataID", "data_hash")
        )

    def make_instance(self, payload):
        return BuoyData(**payload)

    def write(self, to_create, to_update):
        now = timezone.now()

        for obj in to_update:
            obj.updated_at = now

        with transaction.atomic():
            if to_create:
                BuoyData.objects.bulk_create(to_create, batch_size=1000)

            if to_update:
                BuoyData.objects.bulk_update(
                    to_update,
                    fields=self.hash_fields + ["data_hash", "updated_at"],
                    batch_size=1000,
                )
