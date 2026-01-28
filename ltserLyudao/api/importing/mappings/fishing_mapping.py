def build_fishing_payload(record, validators):
    """
    CKAN datastore record -> FishingData payload(dict)
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    eventID = validators["required"](record.get("eventID"), "eventID", record, errors)
    locationID = validators["required"](
        record.get("locationID"), "locationID", record, errors
    )
    verbatimLocality = validators["required"](
        record.get("verbatimLocality"), "verbatimLocality", record, errors
    )

    # 布林值
    is_local_villager = validators["boolean"](
        record.get("is_local_villager"), "is_local_villager", record, errors
    )

    # 日期
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "locationID": locationID,
        "verbatimLocality": verbatimLocality,
        "is_local_villager": is_local_villager,
        "purpose": record.get("purpose"),
        "preferable_site": record.get("preferable_site"),
        "catchment_individuals_per_month": record.get(
            "catchment__individuals_per_month_"
        ),
        "fishing_feq": record.get("fishing_feq"),
        "fishing_method": record.get("fishing_method"),
        "bait": record.get("bait"),
        "fish_species": record.get("fish_species"),
        "feel_size_decrease": record.get("feel_size_decrease"),
    }

    return payload, errors, warnings
