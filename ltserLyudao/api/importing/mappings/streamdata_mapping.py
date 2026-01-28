def build_streamdata_payload(record, validators):
    """
    將 CKAN datastore record 轉成 StreamData 可用的 payload(dict)。
    validators: required/decimal/event_date
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
    locality = validators["required"](
        record.get("locality"), "locality", record, errors
    )

    # DateField（必填）
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "locationID": locationID,
        "locality": locality,
        # float 欄位（允許空）
        "waterTemperature": validators["decimal"](
            record.get("waterTemperature"), "waterTemperature", record, errors, warnings
        ),
        "pH": validators["decimal"](record.get("pH"), "pH", record, errors, warnings),
        "DO": validators["decimal"](record.get("DO"), "DO", record, errors, warnings),
        "conductivity": validators["decimal"](
            record.get("conductivity"), "conductivity", record, errors, warnings
        ),
        "salinity": validators["decimal"](
            record.get("salinity"), "salinity", record, errors, warnings
        ),
        "SS": validators["decimal"](record.get("SS"), "SS", record, errors, warnings),
        # CKAN 可能是 NH3-H / NO2-H / NO3-H / PO4-P
        "NH3_H": validators["decimal"](
            (
                record.get("NH3-H")
                if record.get("NH3-H") is not None
                else record.get("NH3_H")
            ),
            "NH3_H",
            record,
            errors,
            warnings,
        ),
        "NO2_H": validators["decimal"](
            (
                record.get("NO2-H")
                if record.get("NO2-H") is not None
                else record.get("NO2_H")
            ),
            "NO2_H",
            record,
            errors,
            warnings,
        ),
        "NO3_H": validators["decimal"](
            (
                record.get("NO3-H")
                if record.get("NO3-H") is not None
                else record.get("NO3_H")
            ),
            "NO3_H",
            record,
            errors,
            warnings,
        ),
        "PO4_P": validators["decimal"](
            (
                record.get("PO4-P")
                if record.get("PO4-P") is not None
                else record.get("PO4_P")
            ),
            "PO4_P",
            record,
            errors,
            warnings,
        ),
        "BOD5": validators["decimal"](
            record.get("BOD5"), "BOD5", record, errors, warnings
        ),
        "RPI_Score": validators["decimal"](
            record.get("RPI_Score"), "RPI_Score", record, errors, warnings
        ),
        "RPI_Level": record.get("RPI_Level"),
    }

    return payload, errors, warnings
