def build_fishdiv_payload(record, validators):
    """
    將 CKAN datastore record 轉成 FishData 可用的 payload(dict)。
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
    samplingProtocol = validators["required"](
        record.get("samplingProtocol"), "samplingProtocol", record, errors
    )

    # 日期
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 整數欄位
    replicate = validators["int_optional"](
        record.get("replicate"), "replicate", record, errors
    )
    sampleSizeValue = validators["int_optional"](
        record.get("sampleSizeValue"), "sampleSizeValue", record, errors
    )
    individualCount = validators["int_optional"](
        record.get("individualCount"), "individualCount", record, errors
    )

    # 浮點欄位
    bodyLength = validators["decimal"](
        record.get("bodyLength"), "bodyLength", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "season": record.get("season"),
        "locationID": locationID,
        "locality": record.get("locality"),
        "verbatimDepth": record.get("verbatimDepth"),
        "replicate": replicate,
        "sampleSizeValue": sampleSizeValue,
        "sampleSizeUnit": record.get("sampleSizeUnit"),
        "fieldNotes": record.get("fieldNotes"),
        "recordedBy": record.get("recordedBy"),
        "family": record.get("family"),
        "scientificName": record.get("scientificName"),
        "taxonRank": record.get("taxonRank"),
        "bodyLength": bodyLength,
        "samplingProtocol": samplingProtocol,
        "individualCount": individualCount,
        "identifiedBy": record.get("identifiedBy"),
    }

    return payload, errors, warnings
