from django.db import connection, transaction

from api.models import (
    AquaticfaunaData,
    IptAquaticfaunaEvent,
    IptAquaticfaunaOccurrenceExtension,
)


DEFAULT_COUNTRY = "Taiwan"
DEFAULT_COUNTRY_CODE = "TW"
DEFAULT_COUNTY = "Taitung County"
DEFAULT_MUNICIPALITY = "Lyudao Township"
DEFAULT_GEODETIC_DATUM = "WGS84"
DEFAULT_PROTOCOL = "Unknown"
DEFAULT_BASIS_OF_RECORD = "HumanObservation"

LOCALITY_FROM_LOCATION_ID = {
    "DMO": "Dam Outlet",
    "YZHFW1": "Youzihhu Freshwater Waterfall",
    "YZHFW2": "Youzihhu Freshwater Waterfall",
    "DMD": "Dam Downstream",
    "DM": "Dam",
    "DMU": "Dam Upstream",
}

COORDINATES_FROM_LOCATION_ID = {
    "DM": (22.67313119, 121.5005733),
    "DMD": (22.67337807, 121.5007636),
    "DMO": (22.67590546, 121.5013929),
    "DMU": (22.66858039, 121.4977459),
    "YZHFW1": (22.66234022, 121.5079205),
    "YZHFW2": (22.66240237, 121.5081323),
}

SAMPLING_PROTOCOL_MAP = {
    "手抄網(半定量調查)": "Hand-net sampling (semi-quantitative survey)",
    "陷阱法(至多設置一件長城籠及3個蝦籠，視現況水深而定)配合手抄網": "Trap method (up to one fyke net and three shrimp traps, depending on water depth) combined with hand-net sampling",
}


def build_event_id(row):
    if row.eventID:
        return row.eventID
    if row.locationID and row.time:
        return f"AQF-{row.locationID}-{row.time.strftime('%Y%m%d')}"
    if row.time:
        return f"AQF-{row.time.strftime('%Y%m%d')}-{row.pk}"
    return f"AQF-{row.pk}"


def event_date_str(value):
    if value:
        return value.strftime("%Y-%m-%d")
    return ""


def to_locality_en(location_id, fallback_value=None):
    if location_id:
        key = str(location_id).strip().upper()
        if key in LOCALITY_FROM_LOCATION_ID:
            return LOCALITY_FROM_LOCATION_ID[key]
    return fallback_value


def to_sampling_protocol_en(sampling_protocol):
    if not sampling_protocol:
        return DEFAULT_PROTOCOL

    normalized = str(sampling_protocol).strip()
    if normalized in SAMPLING_PROTOCOL_MAP:
        return SAMPLING_PROTOCOL_MAP[normalized]

    compact = normalized.replace(" ", "")
    for raw, mapped in SAMPLING_PROTOCOL_MAP.items():
        if compact == raw.replace(" ", ""):
            return mapped

    return normalized


def to_coordinates(location_id):
    if not location_id:
        return None, None
    key = str(location_id).strip().upper()
    if key in COORDINATES_FROM_LOCATION_ID:
        return COORDINATES_FROM_LOCATION_ID[key]
    return None, None


def aquaticfauna_queryset(limit=None):
    queryset = AquaticfaunaData.objects.all().order_by("id")
    if limit is None:
        return queryset

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        raise ValueError("limit must be an integer")

    if limit <= 0:
        raise ValueError("limit must be > 0")

    return queryset[:limit]


def sync_aquaticfauna_events(dry_run=False, truncate=False, limit=None):
    queryset = aquaticfauna_queryset(limit=limit)

    grouped_events = {}
    for row in queryset:
        event_id = build_event_id(row)
        if event_id not in grouped_events:
            lat, lon = to_coordinates(row.locationID)
            grouped_events[event_id] = {
                "eventDate": event_date_str(row.time),
                "samplingProtocol": to_sampling_protocol_en(row.samplingProtocol),
                "sampleSizeValue": None,
                "sampleSizeUnit": None,
                "samplingEffort": None,
                "locationID": row.locationID,
                "country": DEFAULT_COUNTRY,
                "countryCode": DEFAULT_COUNTRY_CODE,
                "county": DEFAULT_COUNTY,
                "municipality": DEFAULT_MUNICIPALITY,
                "locality": to_locality_en(
                    row.locationID, fallback_value=row.river or row.locationID
                ),
                "verbatimLocality": row.river,
                "decimalLatitude": lat,
                "decimalLongitude": lon,
                "geodeticDatum": DEFAULT_GEODETIC_DATUM,
            }

        group = grouped_events[event_id]
        if row.samplingProtocol and group["samplingProtocol"] == DEFAULT_PROTOCOL:
            group["samplingProtocol"] = to_sampling_protocol_en(row.samplingProtocol)
        if not group["locality"]:
            group["locality"] = to_locality_en(
                row.locationID, fallback_value=row.river or row.locationID
            )
        if group["decimalLatitude"] is None or group["decimalLongitude"] is None:
            lat, lon = to_coordinates(row.locationID)
            if lat is not None and lon is not None:
                group["decimalLatitude"] = lat
                group["decimalLongitude"] = lon
        if row.river and not group["verbatimLocality"]:
            group["verbatimLocality"] = row.river
        if row.locationID and not group["locationID"]:
            group["locationID"] = row.locationID
        if not group["eventDate"] and row.time:
            group["eventDate"] = event_date_str(row.time)

    payloads = []
    skipped_no_event_date = 0
    for event_id, payload in grouped_events.items():
        if not payload["eventDate"]:
            skipped_no_event_date += 1
            continue
        payloads.append((event_id, payload))

    existing_ids = set()
    if not truncate:
        existing_ids = set(IptAquaticfaunaEvent.objects.values_list("eventID", flat=True))

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
                table_name = IptAquaticfaunaEvent._meta.db_table
                with connection.cursor() as cursor:
                    cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY;')

            for event_id, payload in payloads:
                _, created = IptAquaticfaunaEvent.objects.update_or_create(
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
        "source_records": queryset.count() if hasattr(queryset, "count") else 0,
        "grouped_events": len(grouped_events),
        "synced_events": len(payloads),
        "skipped_no_event_date": skipped_no_event_date,
        "created": created_count,
        "updated": updated_count,
    }


def sync_aquaticfauna_occurrence_extensions(dry_run=False, truncate=False, limit=None):
    queryset = aquaticfauna_queryset(limit=limit)

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

        occurrence_payloads[row.dataID] = {
            "eventID": build_event_id(row),
            "basisOfRecord": DEFAULT_BASIS_OF_RECORD,
            "scientificName": row.scientificName,
            "individualCount": row.individualCount,
        }

    existing_ids = set()
    if not truncate:
        existing_ids = set(
            IptAquaticfaunaOccurrenceExtension.objects.values_list(
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
                table_name = IptAquaticfaunaOccurrenceExtension._meta.db_table
                with connection.cursor() as cursor:
                    cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY;')

            for occurrence_id, payload in occurrence_payloads.items():
                _, created = IptAquaticfaunaOccurrenceExtension.objects.update_or_create(
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
        "source_records": queryset.count() if hasattr(queryset, "count") else 0,
        "synced_occurrences": len(occurrence_payloads),
        "skipped_no_occurrence_id": skipped_no_occurrence_id,
        "skipped_no_scientific_name": skipped_no_scientific_name,
        "created": created_count,
        "updated": updated_count,
    }
