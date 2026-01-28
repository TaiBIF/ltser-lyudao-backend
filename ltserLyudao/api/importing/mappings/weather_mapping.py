def build_weather_payload(record, validators):
    """
    將 CKAN datastore record 轉成 WeatherData 可用的 payload(dict)。
    回傳：payload, row_errors, row_warnings
    """
    errors = []
    warnings = []

    # 必填（
    dataID = validators["required"](record.get("dataID"), "dataID", record, errors)
    resourceName = validators["required"](
        record.get("ResourceName"), "resourceName", record, errors
    )
    locationID = validators["required"](
        record.get("locationID"), "locationID", record, errors
    )
    locality = validators["required"](
        record.get("locality"), "locality", record, errors
    )
    stationAttribute = validators["required"](
        record.get("stationAttribute"), "stationAttribute", record, errors
    )
    stationAddress = validators["required"](
        record.get("stationAddress"), "stationAddress", record, errors
    )

    # 日期
    time = validators["event_datetime"](record.get("eventDate"), "time", record, errors)

    # 經緯度
    decimalLongitude = validators["decimal"](
        record.get("decimalLongitude"), "decimalLongitude", record, errors, warnings
    )
    decimalLatitude = validators["decimal"](
        record.get("decimalLatitude"), "decimalLatitude", record, errors, warnings
    )

    # 其餘可為空的數值欄位（FloatField null=True blank=True）
    PAR = validators["decimal"](record.get("PAR"), "PAR", record, errors, warnings)
    solarRadiation = validators["decimal"](
        record.get("SolarRadiation"), "solarRadiation", record, errors, warnings
    )
    windDirection = validators["decimal"](
        record.get("WindDirection"), "windDirection", record, errors, warnings
    )
    pressure = validators["decimal"](
        record.get("Pressure"), "pressure", record, errors, warnings
    )
    windSpeed = validators["decimal"](
        record.get("WindSpeed"), "windSpeed", record, errors, warnings
    )
    gustSpeed = validators["decimal"](
        record.get("GustSpeed"), "gustSpeed", record, errors, warnings
    )
    airTemperature = validators["decimal"](
        record.get("airTemperature"), "airTemperature", record, errors, warnings
    )
    RH = validators["decimal"](record.get("RH"), "RH", record, errors, warnings)
    precipitation = validators["decimal"](
        record.get("precipitation"), "precipitation", record, errors, warnings
    )

    payload = {
        "dataID": dataID,
        "resourceName": resourceName,
        "time": time,
        "locationID": locationID,
        "locality": locality,
        "stationAttribute": stationAttribute,
        "decimalLongitude": decimalLongitude,
        "decimalLatitude": decimalLatitude,
        "stationAddress": stationAddress,
        "PAR": PAR,
        "solarRadiation": solarRadiation,
        "windDirection": windDirection,
        "pressure": pressure,
        "windSpeed": windSpeed,
        "gustSpeed": gustSpeed,
        "airTemperature": airTemperature,
        "RH": RH,
        "precipitation": precipitation,
    }

    return payload, errors, warnings
