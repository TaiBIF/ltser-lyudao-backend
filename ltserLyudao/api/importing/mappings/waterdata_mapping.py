def build_waterdata_payload(record, validators):
    """
    將 CKAN datastore record 轉成 WaterData 可用的 payload(dict)。
    validators 是一組函式集合（避免這個 utils 直接 import Django / settings）
    回傳：
      payload, row_errors, row_warnings
    """

    errors = []
    warnings = []

    # 必填欄位（依你的標準：dataID/eventID/eventDate/locationID）
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    eventID = validators["required"](record.get("eventID"), "eventID", record, errors)
    locationID = validators["required"](
        record.get("locationID"), "locationID", record, errors
    )

    # eventDate → 你目前 model 欄位叫 time（DateField）
    # 這裡先照現況把 eventDate 解析成 date 存到 time
    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 選填欄位
    resourceName = record.get("resourceName")
    locality = record.get("locality")

    # verbatimDepth：你標準其實是字串（如 6-8 m）
    # 但你 model 現在是 FloatField，所以先沿用「轉 float」的做法（會存不下 6-8 m）
    # 若你之後把 model 改成 CharField，這裡就改成原樣存字串 + 格式檢查
    verbatimDepth = validators["decimal"](
        record.get("verbatimDepth"), "verbatimDepth", record, errors, warnings
    )

    # 數值欄位：全部允許空
    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "resourceName": resourceName,
        "time": time,
        "locationID": locationID,
        "locality": locality,
        "verbatimDepth": verbatimDepth,
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
        "turbidity": validators["decimal"](
            record.get("turbidity"), "turbidity", record, errors, warnings
        ),
        "SS": validators["decimal"](record.get("SS"), "SS", record, errors, warnings),
        "NH3_H": validators["decimal"](
            record.get("NH3-H"), "NH3-H", record, errors, warnings
        ),
        "NO2_H": validators["decimal"](
            record.get("NO2-H"), "NO2-H", record, errors, warnings
        ),
        "NO3_H": validators["decimal"](
            record.get("NO3-H"), "NO3-H", record, errors, warnings
        ),
        "PO4_P": validators["decimal"](
            record.get("PO4-P"), "PO4-P", record, errors, warnings
        ),
        "TBC": validators["decimal"](
            record.get("TBC"), "TBC", record, errors, warnings
        ),
        "vibrio": validators["decimal"](
            record.get("vibrio"), "vibrio", record, errors, warnings
        ),
        "COD": validators["decimal"](
            record.get("COD"), "COD", record, errors, warnings
        ),
        "MBAS": validators["decimal"](
            record.get("MBAS"), "MBAS", record, errors, warnings
        ),
        "TOC": validators["decimal"](
            record.get("TOC"), "TOC", record, errors, warnings
        ),
        "Lipid": validators["decimal"](
            record.get("Lipid"), "Lipid", record, errors, warnings
        ),
        "BOD5": validators["decimal"](
            record.get("BOD5"), "BOD5", record, errors, warnings
        ),
    }

    # 如果必填欄位缺失或日期解析失敗，payload 仍會有 None
    # 你可以在 service 層決定：遇到 row error 就跳過不寫 DB
    return payload, errors, warnings
