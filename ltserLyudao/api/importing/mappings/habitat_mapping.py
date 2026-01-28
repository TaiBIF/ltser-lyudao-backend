def build_habitat_payload(record, validators):
    """
    將 CKAN datastore record 轉成 HabitatData 可用的 payload(dict)。
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    eventID = validators["required"](record.get("eventID"), "eventID", record, errors)

    # DateField（必填）
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    season = validators["required"](record.get("Season"), "season", record, errors)
    river = validators["required"](record.get("river"), "river", record, errors)
    locationID = validators["required"](
        record.get("locationID"), "locationID", record, errors
    )
    factor = validators["required"](record.get("Factor"), "factor", record, errors)

    # IntegerField
    score = validators["int"](record.get("Score"), "score", record, errors)

    samplingProtocol = validators["required"](
        record.get("samplingProtocol"), "samplingProtocol", record, errors
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "season": season,
        "river": river,
        "locationID": locationID,
        "factor": factor,
        "score": score,
        "samplingProtocol": samplingProtocol,
    }

    return payload, errors, warnings
