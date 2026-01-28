def build_coralrec_payload(record, validators):
    """
    CKAN datastore record -> CoralData payload(dict)
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

    # 日期
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 整數
    year = validators["int"](record.get("year"), "year", record, errors)
    month = validators["int"](record.get("month"), "month", record, errors)
    day = validators["int"](record.get("day"), "day", record, errors)
    replicate = validators["int"](record.get("replicate"), "replicate", record, errors)
    individualCount = validators["int"](
        record.get("individualCount"), "individualCount", record, errors
    )

    # 小數/浮點
    decimalLatitude = validators["decimal"](
        record.get("decimalLatitude"), "decimalLatitude", record, errors, warnings
    )
    decimalLongitude = validators["decimal"](
        record.get("decimalLongitude"), "decimalLongitude", record, errors, warnings
    )
    measurementValue = validators["decimal"](
        record.get("measurementValue"), "measurementValue", record, errors, warnings
    )
    sampleSizeValue = validators["decimal"](
        record.get("sampleSizeValue"), "sampleSizeValue", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "year": year,
        "month": month,
        "day": day,
        "time": time,
        "locationID": locationID,
        "verbatimLocality": record.get("verbatimLocality"),
        "locality": record.get("locality"),
        "verbatimDepth": record.get("verbatimDepth"),
        "decimalLatitude": decimalLatitude,
        "decimalLongitude": decimalLongitude,
        "replicate": replicate,
        "scientificName": record.get("scientificName"),
        "taxonRank": record.get("taxonRank"),
        "family": record.get("family"),
        "identificationRemarks": record.get("identificationRemarks"),
        "measurementType": record.get("measurementType"),
        "measurementValue": measurementValue,
        "measurementUnit": record.get("measurementUnit"),
        "individualCount": individualCount,
        "recordedBy": record.get("recordedBy"),
        "identifiedBy": record.get("identifiedBy"),
        "samplingProtocol": record.get("samplingProtocol"),
        "sampleSizeValue": sampleSizeValue,
        "sampleSizeUnit": record.get("sampleSizeUnit"),
    }

    return payload, errors, warnings
