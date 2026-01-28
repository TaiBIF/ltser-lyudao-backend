def build_aquaticfauna_payload(record, validators):
    """
    將 CKAN datastore record 轉成 AquaticfaunaData 可用的 payload(dict)。
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

    year = validators["int"](record.get("Year"), "year", record, errors)
    month = validators["int"](record.get("Month"), "month", record, errors)

    individualCount = validators["int"](
        record.get("individualCount"), "individualCount", record, errors
    )

    abundance = validators["decimal"](
        record.get("Abundance"), "abundance", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "eventID": record.get("eventID"),
        "time": time,
        "season": record.get("season"),
        "year": year,
        "month": month,
        "river": record.get("river"),
        "locationID": record.get("locationID"),
        "surveyObjectID": record.get("surveyObjectID"),
        "surveyObject": record.get("surveyObject"),
        "phylum": record.get("phylum"),
        "phylum_c": record.get("phylum_c"),
        "class_field": record.get("class"),
        "class_c": record.get("class_c"),
        "family": record.get("family"),
        "family_c": record.get("family_c"),
        "scientificName": record.get("scientificName"),
        "vernacularName": record.get("vernacularName"),
        "taxonRank": record.get("taxonRank"),
        "individualCount": individualCount,
        "samplingProtocol": record.get("samplingProtocol"),
        "abundance": abundance,
        "abundanceUnit": record.get("AbundanceUnit"),
        "informationWithheld": record.get("informationWithheld"),
    }

    return payload, errors, warnings
