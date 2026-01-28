def build_birdnet_sound_payload(record, validators):
    """
    將 CKAN datastore record 轉成 BirdNetSoundData 可用的 payload(dict)。
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    eventID = validators["required"](record.get("eventID"), "eventID", record, errors)
    scientificName = validators["required"](
        record.get("scientificName"), "scientificName", record, errors
    )

    # 日期（錄音時間）
    time = validators["event_datetime"](record.get("time"), "time", record, errors)

    # 數值欄位
    time_begin = validators["int"](
        record.get("time_begin"), "time_begin", record, errors
    )
    time_end = validators["int"](record.get("time_end"), "time_end", record, errors)

    confidence = validators["decimal"](
        record.get("confidence"), "confidence", record, errors, warnings
    )

    scientificNameID = validators["int"](
        record.get("scientificNameID"), "scientificNameID", record, errors
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "vernacularName": record.get("vernacularName"),
        "model": record.get("model"),
        "time_begin": time_begin,
        "time_end": time_end,
        "confidence": confidence,
        "associatedMedia": record.get("associatedMedia"),
        "time": time,
        "locationID": record.get("locationID"),
        "taxonID": record.get("taxonID"),
        "scientificName": scientificName,
        "taxonRank": record.get("taxonRank"),
        "scientificNameID": scientificNameID,
        "family": record.get("family"),
        "familyChinese": record.get("familyChinese"),
        "birdnet2_4": record.get("birdnet2_4"),
    }

    return payload, errors, warnings
