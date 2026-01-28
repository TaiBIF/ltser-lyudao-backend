def build_zoobenthos_payload(record, validators):
    """
    將 CKAN datastore record 轉成 ZoobenthosData 可用的 payload(dict)。
    validators: required/decimal/event_date
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    eventID = record.get("eventID")
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 字串欄位
    season = record.get("season")
    day_or_night = record.get("day_or_night")
    river = record.get("river")
    locationID = record.get("locationID")
    surveyObjectID = record.get("surveyObjectID")
    surveyObject = record.get("surveyObject")
    phylum = record.get("phylum")
    phylum_c = record.get("phylum_c")
    class_name = record.get("class")
    class_c = record.get("class_c")
    family = record.get("family")
    family_c = record.get("family_c")
    scientificName = record.get("scientificName")
    vernacularName = record.get("vernacularName")
    taxonRank = record.get("taxonRank")
    samplingProtocol = record.get("samplingProtocol")
    habitat = record.get("habitat")
    informationWithheld = record.get("informationWithheld")

    # int 欄位
    year = validators["int"](record.get("Year"), "year", record, errors)
    month = validators["int"](record.get("Month"), "month", record, errors)
    individualCount = validators["int"](
        record.get("individualCount"), "individualCount", record, errors
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "season": season,
        "day_or_night": day_or_night,
        "year": year,
        "month": month,
        "river": river,
        "locationID": locationID,
        "surveyObjectID": surveyObjectID,
        "surveyObject": surveyObject,
        "phylum": phylum,
        "phylum_c": phylum_c,
        "class_name": class_name,
        "class_c": class_c,
        "family": family,
        "family_c": family_c,
        "scientificName": scientificName,
        "vernacularName": vernacularName,
        "taxonRank": taxonRank,
        "individualCount": individualCount,
        "samplingProtocol": samplingProtocol,
        "habitat": habitat,
        "informationWithheld": informationWithheld,
    }

    return payload, errors, warnings
