def build_sea_temperature_payload(record, validators):
    """
    將 CKAN datastore record 轉成 BaseSeaTemperatureData 可用的 payload(dict)。
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    eventID = validators["required"](record.get("eventID"), "eventID", record, errors)
    resourceName = validators["required"](
        record.get("resourceName"), "resourceName", record, errors
    )
    locationID = validators["required"](
        record.get("locationID"), "locationID", record, errors
    )
    verbatimDepth = validators["required"](
        record.get("verbatimDepth"), "verbatimDepth", record, errors
    )

    # 日期
    time = validators["event_datetime"](record.get("eventDate"), "time", record, errors)

    # 選填
    fieldNumber = record.get("fieldNumber")

    # 數值
    seaTemperature = validators["decimal"](
        record.get("seaTemperature"), "seaTemperature", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "resourceName": resourceName,
        "locationID": locationID,
        "verbatimDepth": verbatimDepth,
        "fieldNumber": fieldNumber,
        "time": time,
        "seaTemperature": seaTemperature,
    }

    return payload, errors, warnings
