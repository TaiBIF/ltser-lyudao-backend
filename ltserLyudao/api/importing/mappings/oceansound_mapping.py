def build_ocean_sound_index_payload(record, validators):
    """
    將 CKAN datastore record 轉成 OceanSoundIndexData 可用的 payload(dict)。
    validators: required/decimal/event_date/int
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    eventID = record.get("eventID")
    locationID = record.get("locationID")
    time = validators["event_date"](
        record.get("measurementDeterminedDate"),
        "measurementDeterminedDate",
        record,
        errors,
    )
    verbatimDepth = record.get("verbatimDepth")

    # float 欄位
    kHz0_24 = validators["decimal"](
        record.get("unsafe_0_24khz"), "unsafe_0_24khz", record, errors, warnings
    )
    lower_200Hz = validators["decimal"](
        record.get("lower_200Hz"), "lower_200Hz", record, errors, warnings
    )
    Hz200_1500 = validators["decimal"](
        record.get("unsafe_200_1500hz"), "unsafe_200_1500hz", record, errors, warnings
    )
    higher_1500Hz = validators["decimal"](
        record.get("higher_1500Hz"), "higher_1500Hz", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "locationID": locationID,
        "time": time,
        "kHz0_24": kHz0_24,
        "lower_200Hz": lower_200Hz,
        "Hz200_1500": Hz200_1500,
        "higher_1500Hz": higher_1500Hz,
        "verbatimDepth": verbatimDepth,
    }

    return payload, errors, warnings
