def build_terresoundindex_payload(record, validators):
    """
    將 CKAN datastore record 轉成 TerreSoundIndexData 可用的 payload(dict)
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    payload = {
        "dataID": dataID,
        "eventID": record.get("eventID"),
        "locationID": record.get("locationID"),
        # Float 欄位
        "sh": validators["decimal"](record.get("sh"), "sh", record, errors, warnings),
        "th": validators["decimal"](record.get("th"), "th", record, errors, warnings),
        "H": validators["decimal"](record.get("H"), "H", record, errors, warnings),
        "ACI": validators["decimal"](
            record.get("ACI"), "ACI", record, errors, warnings
        ),
        "ADI": validators["decimal"](
            record.get("ADI"), "ADI", record, errors, warnings
        ),
        "AEI": validators["decimal"](
            record.get("AEI"), "AEI", record, errors, warnings
        ),
        "BI": validators["decimal"](record.get("BI"), "BI", record, errors, warnings),
        "NDSI": validators["decimal"](
            record.get("NDSI"), "NDSI", record, errors, warnings
        ),
        "associatedMedia": record.get("associatedMedia"),
        "min": validators["decimal"](
            record.get("min"), "min", record, errors, warnings
        ),
        "sec": validators["decimal"](
            record.get("sec"), "sec", record, errors, warnings
        ),
        # DateTimeField
        "time": validators["event_datetime"](
            record.get("measurementDeterminedDate"),
            "measurementDeterminedDate",
            record,
            errors,
        ),
    }

    return payload, errors, warnings
