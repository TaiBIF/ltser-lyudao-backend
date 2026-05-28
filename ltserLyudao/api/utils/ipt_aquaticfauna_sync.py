import re

import requests

from django.db import connection, transaction

from api.models import (
    AquaticfaunaData,
    IptAquaticfaunaEvent,
    IptAquaticfaunaOccurrenceExtension,
    ZoobenthosData,
)

DEFAULT_COUNTRY = "Taiwan"
DEFAULT_COUNTRY_CODE = "TW"
DEFAULT_COUNTY = "Taitung County"
DEFAULT_MUNICIPALITY = "Lyudao Township"
DEFAULT_GEODETIC_DATUM = "WGS84"
DEFAULT_PROTOCOL = "Unknown"
DEFAULT_BASIS_OF_RECORD = "HumanObservation"
DEFAULT_KINGDOM = "Animalia"
NOMENMATCH_URL = "https://match.taibif.tw/v2/api.php"
NOMENMATCH_CHUNK_SIZE = 20
NOMENMATCH_TIMEOUT = 30

LOCALITY_FROM_LOCATION_ID = {
    "DMO": "Dam Outlet",
    "YZHFW1": "Youzihhu Freshwater Waterfall",
    "YZHFW2": "Youzihhu Freshwater Waterfall",
    "DMD": "Dam Downstream",
    "DM": "Dam",
    "DMU": "Dam Upstream",
    "CK": "Chaikou",
    "LHI": "Lighthouse - intertidal zone",
    "YZH": "Youzihhu",
    "DMM": "Dam Outlet - Marine zone",
}

COORDINATES_FROM_LOCATION_ID = {
    "DM": (22.67313119, 121.5005733),
    "DMD": (22.67337807, 121.5007636),
    "DMO": (22.67590546, 121.5013929),
    "DMU": (22.66858039, 121.4977459),
    "YZHFW1": (22.66234022, 121.5079205),
    "YZHFW2": (22.66240237, 121.5081323),
    "CK": (22.677954, 121.482352),
    "LHI": (22.67738678, 121.4665535),
    "YZH": (22.665674, 121.510054),
    "DMM": (22.67634799, 121.5001978),
}

SAMPLING_PROTOCOL_MAP = {
    "手抄網(半定量調查)": "Hand-net sampling (semi-quantitative survey)",
    "陷阱法(至多設置一件長城籠及3個蝦籠，視現況水深而定)配合手抄網": "Trap method (up to one fyke net and three shrimp traps, depending on water depth) combined with hand-net sampling",
    "定量(1m2樣框)": "Quantitative sampling (1 m2 quadrat)",
    "普查": "Census survey",
}

SOURCE_MODELS = (AquaticfaunaData, ZoobenthosData)


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


def row_class_value(row):
    return getattr(row, "class_field", None) or getattr(row, "class_name", None)


def normalize_taxon_name(value):
    if not value:
        return ""
    normalized = str(value).strip()
    normalized = re.sub(r"(?i)(^|\s)spp?\.?(?=\s|$)", " ", normalized)
    return " ".join(normalized.split())


def lowercase_taxon_rank(value):
    if not value:
        return None
    return str(value).strip().lower()


def chunked(values, size):
    for index in range(0, len(values), size):
        yield values[index : index + size]


def iter_taibif_match_items(value):
    if isinstance(value, dict):
        if "results" in value:
            yield value
        return

    if isinstance(value, list):
        for item in value:
            yield from iter_taibif_match_items(item)


def taxon_payload_from_result(result):
    accepted_namecode = result.get("accepted_namecode")
    parent_name_usage_id = None
    if accepted_namecode:
        parent_name_usage_id = f"{accepted_namecode}(TaiCOL)"

    return {
        "kingdom": result.get("kingdom") or DEFAULT_KINGDOM,
        "phylum": result.get("phylum"),
        "class_field": result.get("class"),
        "order": result.get("order"),
        "family": result.get("family"),
        "genus": result.get("genus"),
        "taxonRank": result.get("taxon_rank"),
        "parentNameUsageID": parent_name_usage_id,
    }


def select_nomenmatch_result(results):
    for result in results:
        if str(result.get("kingdom") or "").strip().lower() == "animalia":
            return result
    return results[0]


def fetch_nomenmatch_taxon_map(scientific_names):
    taxon_map = {}
    errors = []
    names = sorted({normalize_taxon_name(name) for name in scientific_names if name})

    for names_chunk in chunked(names, NOMENMATCH_CHUNK_SIZE):
        try:
            response = requests.get(
                NOMENMATCH_URL,
                params={
                    "format": "json",
                    "best": "yes",
                    "source": "taicol",
                    "names": "|".join(names_chunk),
                },
                timeout=NOMENMATCH_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as exc:
            errors.append({"names": names_chunk, "error": str(exc)})
            continue
        except ValueError as exc:
            errors.append({"names": names_chunk, "error": f"invalid_json: {exc}"})
            continue

        for item in iter_taibif_match_items(payload.get("data")):
            results = item.get("results") or []
            if not results:
                continue

            result = select_nomenmatch_result(results)
            taxon_payload = taxon_payload_from_result(result)
            for key in (
                item.get("search_term"),
                item.get("name_cleaned"),
                item.get("matched_clean"),
                result.get("simple_name"),
            ):
                normalized = normalize_taxon_name(key)
                if normalized:
                    taxon_map[normalized] = taxon_payload

    return taxon_map, errors


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


def aquaticfauna_querysets(limit=None):
    limit = validate_limit(limit)
    querysets = []
    for model in SOURCE_MODELS:
        queryset = model.objects.all().order_by("id")
        if limit is not None:
            queryset = queryset[:limit]
        querysets.append(queryset)
    return querysets


def iter_aquaticfauna_rows(querysets):
    for queryset in querysets:
        yield from queryset


def source_record_count(querysets):
    return sum(
        queryset.count() if hasattr(queryset, "count") else 0 for queryset in querysets
    )


def aquaticfauna_scientific_names(limit=None):
    limit = validate_limit(limit)
    names = set()

    for model in SOURCE_MODELS:
        queryset = model.objects.exclude(scientificName__isnull=True).exclude(
            scientificName=""
        )

        if limit is None:
            values = (
                queryset.order_by("scientificName")
                .values_list("scientificName", flat=True)
                .distinct()
            )
        else:
            values = queryset.order_by("id").values_list("scientificName", flat=True)[
                :limit
            ]

        for name in values:
            normalized = normalize_taxon_name(name)
            if normalized:
                names.add(normalized)

    return names


def sync_aquaticfauna_events(dry_run=False, truncate=False, limit=None):
    querysets = aquaticfauna_querysets(limit=limit)

    grouped_events = {}
    for row in iter_aquaticfauna_rows(querysets):
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
        existing_ids = set(
            IptAquaticfaunaEvent.objects.values_list("eventID", flat=True)
        )

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
        "source_records": source_record_count(querysets),
        "grouped_events": len(grouped_events),
        "synced_events": len(payloads),
        "skipped_no_event_date": skipped_no_event_date,
        "created": created_count,
        "updated": updated_count,
    }


def sync_aquaticfauna_occurrence_extensions(dry_run=False, truncate=False, limit=None):
    querysets = aquaticfauna_querysets(limit=limit)
    requested_taxon_names = aquaticfauna_scientific_names(limit=limit)
    taxon_map, taxon_lookup_errors = fetch_nomenmatch_taxon_map(requested_taxon_names)

    occurrence_payloads = {}
    skipped_no_occurrence_id = 0
    skipped_no_scientific_name = 0

    for row in iter_aquaticfauna_rows(querysets):
        if not row.dataID:
            skipped_no_occurrence_id += 1
            continue
        if not row.scientificName:
            skipped_no_scientific_name += 1
            continue

        taxon = taxon_map.get(normalize_taxon_name(row.scientificName)) or {}
        lat, lon = to_coordinates(row.locationID)
        occurrence_payloads[row.dataID] = {
            "eventID": build_event_id(row),
            "basisOfRecord": DEFAULT_BASIS_OF_RECORD,
            "scientificName": row.scientificName,
            "individualCount": row.individualCount,
            "eventDate": event_date_str(row.time),
            "decimalLatitude": lat,
            "decimalLongitude": lon,
            "kingdom": taxon.get("kingdom") or DEFAULT_KINGDOM,
            "phylum": taxon.get("phylum") or row.phylum,
            "class_field": taxon.get("class_field") or row_class_value(row),
            "order": taxon.get("order"),
            "family": taxon.get("family") or row.family,
            "genus": taxon.get("genus"),
            "taxonRank": taxon.get("taxonRank") or lowercase_taxon_rank(row.taxonRank),
            "parentNameUsageID": taxon.get("parentNameUsageID"),
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
                _, created = (
                    IptAquaticfaunaOccurrenceExtension.objects.update_or_create(
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
        "source_records": source_record_count(querysets),
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
