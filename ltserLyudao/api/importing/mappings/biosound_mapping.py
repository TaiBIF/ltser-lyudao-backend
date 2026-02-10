def build_biosound_payload(record, validators):
    """
    將 CKAN datastore record 轉成 BioSoundData 可用的 payload(dict)。
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    payload = {
        "dataID": dataID,
        "eventID": record.get("eventID"),
        "locationID": record.get("locationID"),
        # int
        "classid": validators["int"](record.get("classid"), "classid", record, errors),
        "time_begin": validators["int"](
            record.get("time_begin"), "time_begin", record, errors
        ),
        "time_end": validators["int"](
            record.get("time_end"), "time_end", record, errors
        ),
        "freq_low": validators["int"](
            record.get("freq_low"), "freq_low", record, errors
        ),
        "freq_high": validators["int"](
            record.get("freq_high"), "freq_high", record, errors
        ),
        # float
        "confidence": validators["decimal"](
            record.get("confidence"), "confidence", record, errors, warnings
        ),
        # string
        "scientificName": record.get("scientificName"),
        "taxonRank": record.get("taxonRank"),
        "vernacularName": record.get("vernacularName"),
        "soundclass": record.get("soundclass"),
        "associatedMedia": record.get("associatedMedia"),
        # datetime
        "time": validators["event_datetime"](
            record.get("measurementDeterminedDate"),
            "measurementDeterminedDate",
            record,
            errors,
        ),
    }

    return payload, errors, warnings
