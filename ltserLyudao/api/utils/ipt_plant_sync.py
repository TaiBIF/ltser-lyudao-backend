from django.db import connection, transaction

from api.models import (
    PlantData,
    IptPlantEvent,
    IptPlantMeasurementOrFactExtension,
    IptPlantOccurrenceExtension,
)
from api.utils.ipt_aquaticfauna_sync import (
    fetch_nomenmatch_taxon_map,
    normalize_taxon_name,
)


DEFAULT_COUNTRY = "Taiwan"
DEFAULT_COUNTRY_CODE = "TW"
DEFAULT_COUNTY = "Taitung County"
DEFAULT_MUNICIPALITY = "Lyudao Township"
DEFAULT_GEODETIC_DATUM = "WGS84"
DEFAULT_PROTOCOL = "Unknown"
DEFAULT_BASIS_OF_RECORD = "HumanObservation"
DEFAULT_KINGDOM = "Plantae"


def validate_limit(limit):
    if limit is None:
        return None

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        raise ValueError("limit must be an integer")

    if limit <= 0:
        raise ValueError("limit must be > 0")

    return limit


def plant_queryset(limit=None):
    limit = validate_limit(limit)
    queryset = PlantData.objects.all().order_by("id")
    if limit is not None:
        queryset = queryset[:limit]
    return queryset


def build_event_id(row):
    if row.eventID:
        return row.eventID
    if row.locationID and row.time:
        return f"PLANT-{row.locationID}-{row.time.strftime('%Y%m%d')}"
    if row.time:
        return f"PLANT-{row.time.strftime('%Y%m%d')}-{row.pk}"
    return f"PLANT-{row.pk}"


def date_str(value):
    if value:
        return value.strftime("%Y-%m-%d")
    return ""


def lowercase_taxon_rank(value):
    if not value:
        return None
    return str(value).strip().lower()


def truncate_model_table(model):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY;')


def sync_plant_events(dry_run=False, truncate=False, limit=None):
    queryset = plant_queryset(limit=limit)
    grouped_events = {}

    for row in queryset:
        event_id = build_event_id(row)
        if event_id not in grouped_events:
            grouped_events[event_id] = {
                "eventDate": date_str(row.time),
                "samplingProtocol": row.samplingProtocol or DEFAULT_PROTOCOL,
                "sampleSizeValue": row.sampleSizeValue,
                "sampleSizeUnit": row.sampleSizeUnit,
                "samplingEffort": None,
                "locationID": row.locationID,
                "country": DEFAULT_COUNTRY,
                "countryCode": DEFAULT_COUNTRY_CODE,
                "county": DEFAULT_COUNTY,
                "municipality": DEFAULT_MUNICIPALITY,
                "locality": None,
                "verbatimLocality": None,
                "decimalLatitude": row.decimalLatitude,
                "decimalLongitude": row.decimalLongitude,
                "geodeticDatum": DEFAULT_GEODETIC_DATUM,
                "coordinatePrecision": row.coordinatePrecision,
                "verbatimElevation": row.verbatimElevation or "",
            }
            continue

        event = grouped_events[event_id]
        fallback_fields = (
            "sampleSizeValue",
            "sampleSizeUnit",
            "locationID",
            "decimalLatitude",
            "decimalLongitude",
            "coordinatePrecision",
            "verbatimElevation",
        )
        for field_name in fallback_fields:
            value = getattr(row, field_name)
            if value not in (None, "") and event[field_name] in (None, ""):
                event[field_name] = value
        if (
            row.samplingProtocol
            and event["samplingProtocol"] == DEFAULT_PROTOCOL
        ):
            event["samplingProtocol"] = row.samplingProtocol
        if not event["eventDate"] and row.time:
            event["eventDate"] = date_str(row.time)

    payloads = []
    skipped_no_event_date = 0
    for event_id, payload in grouped_events.items():
        if not payload["eventDate"]:
            skipped_no_event_date += 1
            continue
        payloads.append((event_id, payload))

    existing_ids = set()
    if not truncate:
        existing_ids = set(IptPlantEvent.objects.values_list("eventID", flat=True))

    created_count = 0
    updated_count = 0

    if dry_run:
        for event_id, _payload in payloads:
            if event_id in existing_ids:
                updated_count += 1
            else:
                created_count += 1
    else:
        with transaction.atomic():
            if truncate:
                truncate_model_table(IptPlantEvent)

            for event_id, payload in payloads:
                _, created = IptPlantEvent.objects.update_or_create(
                    eventID=event_id,
                    defaults=payload.copy(),
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

    return {
        "dry_run": dry_run,
        "truncate": truncate,
        "source_records": queryset.count(),
        "grouped_events": len(grouped_events),
        "synced_events": len(payloads),
        "skipped_no_event_date": skipped_no_event_date,
        "created": created_count,
        "updated": updated_count,
    }


def sync_plant_occurrence_extensions(dry_run=False, truncate=False, limit=None):
    queryset = plant_queryset(limit=limit)
    requested_taxon_names = {
        normalize_taxon_name(row.scientificName)
        for row in queryset
        if row.scientificName
    }
    taxon_map, taxon_lookup_errors = fetch_nomenmatch_taxon_map(
        requested_taxon_names,
        kingdom=DEFAULT_KINGDOM,
        strict_kingdom=True,
    )
    occurrence_payloads = {}
    skipped_no_occurrence_id = 0
    skipped_no_scientific_name = 0

    for row in queryset:
        if not row.dataID:
            skipped_no_occurrence_id += 1
            continue
        if not row.scientificName:
            skipped_no_scientific_name += 1
            continue

        taxon = taxon_map.get(normalize_taxon_name(row.scientificName)) or {}
        occurrence_payloads[row.dataID] = {
            "eventID": build_event_id(row),
            "basisOfRecord": DEFAULT_BASIS_OF_RECORD,
            "scientificName": row.scientificName,
            "individualCount": None,
            "decimalLatitude": row.decimalLatitude,
            "decimalLongitude": row.decimalLongitude,
            "eventDate": date_str(row.time),
            "kingdom": taxon.get("kingdom") or DEFAULT_KINGDOM,
            "phylum": taxon.get("phylum"),
            "class_field": taxon.get("class_field"),
            "order": taxon.get("order"),
            "family": taxon.get("family") or row.family,
            "genus": taxon.get("genus"),
            "taxonRank": taxon.get("taxonRank")
            or lowercase_taxon_rank(row.taxonRank),
            "acceptedNameUsageID": taxon.get("acceptedNameUsageID"),
            "recordedBy": row.recordedBy,
            "identifiedBy": row.identifiedBy,
        }

    existing_ids = set()
    if not truncate:
        existing_ids = set(
            IptPlantOccurrenceExtension.objects.values_list(
                "occurrenceID", flat=True
            )
        )

    created_count = 0
    updated_count = 0

    if dry_run:
        for occurrence_id in occurrence_payloads:
            if occurrence_id in existing_ids:
                updated_count += 1
            else:
                created_count += 1
    else:
        with transaction.atomic():
            if truncate:
                truncate_model_table(IptPlantOccurrenceExtension)

            for occurrence_id, payload in occurrence_payloads.items():
                _, created = IptPlantOccurrenceExtension.objects.update_or_create(
                    occurrenceID=occurrence_id,
                    defaults=payload.copy(),
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

    return {
        "dry_run": dry_run,
        "truncate": truncate,
        "source_records": queryset.count(),
        "synced_occurrences": len(occurrence_payloads),
        "skipped_no_occurrence_id": skipped_no_occurrence_id,
        "skipped_no_scientific_name": skipped_no_scientific_name,
        "taxon_names_requested": len(requested_taxon_names),
        "taxon_names_matched": len(
            {name for name in requested_taxon_names if name in taxon_map}
        ),
        "taxon_lookup_errors": len(taxon_lookup_errors),
        "created": created_count,
        "updated": updated_count,
    }


def sync_plant_measurement_or_fact_extensions(
    dry_run=False, truncate=False, limit=None
):
    queryset = plant_queryset(limit=limit)
    measurement_payloads = {}
    skipped_no_occurrence_id = 0
    skipped_no_measurement_type = 0
    skipped_no_measurement_value = 0

    for row in queryset:
        if not row.dataID:
            skipped_no_occurrence_id += 1
            continue
        if not row.measurementType:
            skipped_no_measurement_type += 1
            continue
        if row.measurementValue is None:
            skipped_no_measurement_value += 1
            continue

        measurement_payloads[row.dataID] = {
            "eventID": build_event_id(row),
            "measurementType": row.measurementType,
            "measurementValue": str(row.measurementValue),
            "measurementUnit": row.measurementUnit or "",
            "measurementDeterminedDate": date_str(
                row.measurementDeterminedDate
            ),
        }

    existing_ids = set()
    if not truncate:
        existing_ids = set(
            IptPlantMeasurementOrFactExtension.objects.values_list(
                "occurrenceID", flat=True
            )
        )

    created_count = 0
    updated_count = 0

    if dry_run:
        for occurrence_id in measurement_payloads:
            if occurrence_id in existing_ids:
                updated_count += 1
            else:
                created_count += 1
    else:
        with transaction.atomic():
            if truncate:
                truncate_model_table(IptPlantMeasurementOrFactExtension)

            for occurrence_id, payload in measurement_payloads.items():
                _, created = (
                    IptPlantMeasurementOrFactExtension.objects.update_or_create(
                        occurrenceID=occurrence_id,
                        defaults=payload.copy(),
                    )
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

    return {
        "dry_run": dry_run,
        "truncate": truncate,
        "source_records": queryset.count(),
        "synced_measurements": len(measurement_payloads),
        "skipped_no_occurrence_id": skipped_no_occurrence_id,
        "skipped_no_measurement_type": skipped_no_measurement_type,
        "skipped_no_measurement_value": skipped_no_measurement_value,
        "created": created_count,
        "updated": updated_count,
    }
