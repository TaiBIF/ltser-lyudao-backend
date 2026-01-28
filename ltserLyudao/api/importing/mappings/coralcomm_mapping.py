def build_coralcomm_payload(record, validators):
    """
    CKAN datastore record -> CoralCommData payload(dict)
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    # 日期
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 整數欄位
    year = validators["int"](record.get("year"), "year", record, errors)
    month = validators["int"](record.get("month"), "month", record, errors)
    day = validators["int"](record.get("day"), "day", record, errors)
    sampleSizeValue = validators["int"](
        record.get("sampleSizeValue"), "sampleSizeValue", record, errors
    )

    # 浮點欄位
    decimalLatitude = validators["decimal"](
        record.get("decimalLatitude"), "decimalLatitude", record, errors, warnings
    )
    decimalLongitude = validators["decimal"](
        record.get("decimalLongitude"), "decimalLongitude", record, errors, warnings
    )
    coverInPercentage = validators["decimal"](
        record.get("coverInPercentage"), "coverInPercentage", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": record.get("eventID"),
        "year": year,
        "month": month,
        "day": day,
        "time": time,
        "locationID": record.get("locationID"),
        "verbatimLocality": record.get("verbatimLocality"),
        "locality": record.get("locality"),
        "verbatimDepth": record.get("verbatimDepth"),
        "decimalLatitude": decimalLatitude,
        "decimalLongitude": decimalLongitude,
        "replicate": record.get("replicate"),
        "Benthic_group": record.get("Benthic_group"),
        "Benthic_subgroup": record.get("Benthic_subgroup"),
        "coverInPercentage": coverInPercentage,
        "Field_codes_on_CPCe": record.get("field_codes_on_cpce"),
        "samplingProtocol": record.get("samplingProtocol"),
        "sampleSizeValue": sampleSizeValue,
        "sampleSizeUnit": record.get("sampleSizeUnit"),
    }

    return payload, errors, warnings
