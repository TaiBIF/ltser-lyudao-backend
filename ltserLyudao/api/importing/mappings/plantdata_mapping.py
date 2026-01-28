def build_plantdata_payload(record, validators):
    """
    將 CKAN datastore record 轉成 PlantData 可用的 payload(dict)。
    validators: required/decimal/event_date
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填（最少 dataID）
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)

    # 其他欄位（多數允許空）
    eventID = record.get("eventID")

    # 日期欄位（DateField）
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )
    measurementDeterminedDate = validators["event_date"](
        record.get("measurementDeterminedDate"),
        "measurementDeterminedDate",
        record,
        errors,
    )

    locationID = record.get("locationID")
    habitat = record.get("habitat")
    samplingProtocol = record.get("samplingProtocol")
    sampleSizeUnit = record.get("sampleSizeUnit")
    verbatimElevation = record.get("verbatimElevation")

    family = record.get("family")
    scientificName = record.get("scientificName")
    vernacularName = record.get("vernacularName")
    taxonRank = record.get("taxonRank")
    recordedBy = record.get("recordedBy")
    identifiedBy = record.get("identifiedBy")

    measurementType = record.get("measurementType")
    measurementUnit = record.get("measurementUnit")
    layer = record.get("layer")

    # 數值（FloatField）
    decimalLatitude = validators["decimal"](
        record.get("decimalLatitude"), "decimalLatitude", record, errors, warnings
    )
    decimalLongitude = validators["decimal"](
        record.get("decimalLongitude"), "decimalLongitude", record, errors, warnings
    )
    coordinatePrecision = validators["decimal"](
        record.get("coordinatePrecision"),
        "coordinatePrecision",
        record,
        errors,
        warnings,
    )
    measurementValue = validators["decimal"](
        record.get("measurementValue"), "measurementValue", record, errors, warnings
    )

    # sampleSizeValue（IntegerField）
    raw_ssv = record.get("sampleSizeValue")
    sampleSizeValue = None
    if raw_ssv in (None, "", "null"):
        sampleSizeValue = None
    else:
        # 先走 decimal validator，讓它處理 "1", "1.0", " 2 " 這種
        v = validators["decimal"](raw_ssv, "sampleSizeValue", record, errors, warnings)
        if v is None:
            sampleSizeValue = None
        else:
            try:
                # 避免 1.2 這種塞進 int
                fv = float(v)
                if fv.is_integer():
                    sampleSizeValue = int(fv)
                else:
                    warnings.append(
                        {
                            "field": "sampleSizeValue",
                            "warning": "not_integer",
                            "value": raw_ssv,
                        }
                    )
                    sampleSizeValue = None
            except Exception:
                warnings.append(
                    {
                        "field": "sampleSizeValue",
                        "warning": "invalid_integer",
                        "value": raw_ssv,
                    }
                )
                sampleSizeValue = None

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "time": time,
        "locationID": locationID,
        "habitat": habitat,
        "samplingProtocol": samplingProtocol,
        "sampleSizeValue": sampleSizeValue,
        "sampleSizeUnit": sampleSizeUnit,
        "decimalLatitude": decimalLatitude,
        "decimalLongitude": decimalLongitude,
        "coordinatePrecision": coordinatePrecision,
        "verbatimElevation": verbatimElevation,
        "family": family,
        "scientificName": scientificName,
        "vernacularName": vernacularName,
        "taxonRank": taxonRank,
        "recordedBy": recordedBy,
        "identifiedBy": identifiedBy,
        "measurementType": measurementType,
        "measurementValue": measurementValue,
        "measurementUnit": measurementUnit,
        "layer": layer,
        "measurementDeterminedDate": measurementDeterminedDate,
    }

    return payload, errors, warnings
