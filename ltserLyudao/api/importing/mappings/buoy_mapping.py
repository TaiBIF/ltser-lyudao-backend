def build_buoy_payload(record, validators):
    """
    將 CKAN datastore record 轉成 BuoyData 可用的 payload(dict)。
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

    time = validators["event_date"](
        record.get("eventDate"), "eventDate", record, errors
    )

    # 數值欄位
    underwater_par = validators["decimal"](
        record.get("Underwater PAR"), "underwater_par", record, errors, warnings
    )
    terrestrial_par = validators["decimal"](
        record.get("Terrestrial PAR"), "terrestrial_par", record, errors, warnings
    )
    exo_temperature = validators["decimal"](
        record.get("EXO Temperature"), "exo_temperature", record, errors, warnings
    )
    sp_cond = validators["decimal"](
        record.get("Sp Cond"), "sp_cond", record, errors, warnings
    )
    salinity = validators["decimal"](
        record.get("Salinity"), "salinity", record, errors, warnings
    )
    ph = validators["decimal"](record.get("pH"), "ph", record, errors, warnings)
    odo_sat = validators["decimal"](
        record.get("ODOSat"), "odo_sat", record, errors, warnings
    )
    odo = validators["decimal"](record.get("ODO"), "odo", record, errors, warnings)
    aquadopp_temperature = validators["decimal"](
        record.get("Aquadopp Temperature"),
        "aquadopp_temperature",
        record,
        errors,
        warnings,
    )
    corrected_wind_direction = validators["decimal"](
        record.get("Corrected Wind Direction"),
        "corrected_wind_direction",
        record,
        errors,
        warnings,
    )
    corrected_wind_speed = validators["decimal"](
        record.get("Corrected Wind Speed"),
        "corrected_wind_speed",
        record,
        errors,
        warnings,
    )
    air_temperature = validators["decimal"](
        record.get("Air Temperature"), "air_temperature", record, errors, warnings
    )
    relative_humidity = validators["decimal"](
        record.get("Relative Humidity"), "relative_humidity", record, errors, warnings
    )
    barometric_pressure = validators["decimal"](
        record.get("Barometric Pressure"),
        "barometric_pressure",
        record,
        errors,
        warnings,
    )
    precipitation_intensity = validators["decimal"](
        record.get("Precipitation Intensity"),
        "precipitation_intensity",
        record,
        errors,
        warnings,
    )
    precipitation_total = validators["decimal"](
        record.get("Precipitation Total"),
        "precipitation_total",
        record,
        errors,
        warnings,
    )
    wmo_average_wind_direction = validators["decimal"](
        record.get("WMO Average Wind Direction"),
        "wmo_average_wind_direction",
        record,
        errors,
        warnings,
    )
    wmo_average_wind_speed = validators["decimal"](
        record.get("WMO Average Wind Speed"),
        "wmo_average_wind_speed",
        record,
        errors,
        warnings,
    )
    latitude = validators["decimal"](
        record.get("latitude"), "Latitude", record, errors, warnings
    )
    longitude = validators["decimal"](
        record.get("longitude"), "Longitude", record, errors, warnings
    )

    # cell 1~10 currents
    vel_e_cell_1 = validators["decimal"](
        record.get("vel_e_cell_1"), "vel_e_cell_1", record, errors, warnings
    )
    vel_n_cell_1 = validators["decimal"](
        record.get("vel_n_cell_1"), "vel_n_cell_1", record, errors, warnings
    )
    vel_u_cell_1 = validators["decimal"](
        record.get("vel_u_cell_1"), "vel_u_cell_1", record, errors, warnings
    )
    current_speed_1 = validators["decimal"](
        record.get("current_speed_1"), "current_speed_1", record, errors, warnings
    )
    current_direction_1 = validators["decimal"](
        record.get("current_direction_1"),
        "current_direction_1",
        record,
        errors,
        warnings,
    )

    vel_e_cell_2 = validators["decimal"](
        record.get("vel_e_cell_2"), "vel_e_cell_2", record, errors, warnings
    )
    vel_n_cell_2 = validators["decimal"](
        record.get("vel_n_cell_2"), "vel_n_cell_2", record, errors, warnings
    )
    vel_u_cell_2 = validators["decimal"](
        record.get("vel_u_cell_2"), "vel_u_cell_2", record, errors, warnings
    )
    current_speed_2 = validators["decimal"](
        record.get("current_speed_2"), "current_speed_2", record, errors, warnings
    )
    current_direction_2 = validators["decimal"](
        record.get("current_direction_2"),
        "current_direction_2",
        record,
        errors,
        warnings,
    )

    vel_e_cell_3 = validators["decimal"](
        record.get("vel_e_cell_3"), "vel_e_cell_3", record, errors, warnings
    )
    vel_n_cell_3 = validators["decimal"](
        record.get("vel_n_cell_3"), "vel_n_cell_3", record, errors, warnings
    )
    vel_u_cell_3 = validators["decimal"](
        record.get("vel_u_cell_3"), "vel_u_cell_3", record, errors, warnings
    )
    current_speed_3 = validators["decimal"](
        record.get("current_speed_3"), "current_speed_3", record, errors, warnings
    )
    current_direction_3 = validators["decimal"](
        record.get("current_direction_3"),
        "current_direction_3",
        record,
        errors,
        warnings,
    )

    vel_e_cell_4 = validators["decimal"](
        record.get("vel_e_cell_4"), "vel_e_cell_4", record, errors, warnings
    )
    vel_n_cell_4 = validators["decimal"](
        record.get("vel_n_cell_4"), "vel_n_cell_4", record, errors, warnings
    )
    vel_u_cell_4 = validators["decimal"](
        record.get("vel_u_cell_4"), "vel_u_cell_4", record, errors, warnings
    )
    current_speed_4 = validators["decimal"](
        record.get("current_speed_4"), "current_speed_4", record, errors, warnings
    )
    current_direction_4 = validators["decimal"](
        record.get("current_direction_4"),
        "current_direction_4",
        record,
        errors,
        warnings,
    )

    vel_e_cell_5 = validators["decimal"](
        record.get("vel_e_cell_5"), "vel_e_cell_5", record, errors, warnings
    )
    vel_n_cell_5 = validators["decimal"](
        record.get("vel_n_cell_5"), "vel_n_cell_5", record, errors, warnings
    )
    vel_u_cell_5 = validators["decimal"](
        record.get("vel_u_cell_5"), "vel_u_cell_5", record, errors, warnings
    )
    current_speed_5 = validators["decimal"](
        record.get("current_speed_5"), "current_speed_5", record, errors, warnings
    )
    current_direction_5 = validators["decimal"](
        record.get("current_direction_5"),
        "current_direction_5",
        record,
        errors,
        warnings,
    )

    vel_e_cell_6 = validators["decimal"](
        record.get("vel_e_cell_6"), "vel_e_cell_6", record, errors, warnings
    )
    vel_n_cell_6 = validators["decimal"](
        record.get("vel_n_cell_6"), "vel_n_cell_6", record, errors, warnings
    )
    vel_u_cell_6 = validators["decimal"](
        record.get("vel_u_cell_6"), "vel_u_cell_6", record, errors, warnings
    )
    current_speed_6 = validators["decimal"](
        record.get("current_speed_6"), "current_speed_6", record, errors, warnings
    )
    current_direction_6 = validators["decimal"](
        record.get("current_direction_6"),
        "current_direction_6",
        record,
        errors,
        warnings,
    )

    vel_e_cell_7 = validators["decimal"](
        record.get("vel_e_cell_7"), "vel_e_cell_7", record, errors, warnings
    )
    vel_n_cell_7 = validators["decimal"](
        record.get("vel_n_cell_7"), "vel_n_cell_7", record, errors, warnings
    )
    vel_u_cell_7 = validators["decimal"](
        record.get("vel_u_cell_7"), "vel_u_cell_7", record, errors, warnings
    )
    current_speed_7 = validators["decimal"](
        record.get("current_speed_7"), "current_speed_7", record, errors, warnings
    )
    current_direction_7 = validators["decimal"](
        record.get("current_direction_7"),
        "current_direction_7",
        record,
        errors,
        warnings,
    )

    vel_e_cell_8 = validators["decimal"](
        record.get("vel_e_cell_8"), "vel_e_cell_8", record, errors, warnings
    )
    vel_n_cell_8 = validators["decimal"](
        record.get("vel_n_cell_8"), "vel_n_cell_8", record, errors, warnings
    )
    vel_u_cell_8 = validators["decimal"](
        record.get("vel_u_cell_8"), "vel_u_cell_8", record, errors, warnings
    )
    current_speed_8 = validators["decimal"](
        record.get("current_speed_8"), "current_speed_8", record, errors, warnings
    )
    current_direction_8 = validators["decimal"](
        record.get("current_direction_8"),
        "current_direction_8",
        record,
        errors,
        warnings,
    )

    vel_e_cell_9 = validators["decimal"](
        record.get("vel_e_cell_9"), "vel_e_cell_9", record, errors, warnings
    )
    vel_n_cell_9 = validators["decimal"](
        record.get("vel_n_cell_9"), "vel_n_cell_9", record, errors, warnings
    )
    vel_u_cell_9 = validators["decimal"](
        record.get("vel_u_cell_9"), "vel_u_cell_9", record, errors, warnings
    )
    current_speed_9 = validators["decimal"](
        record.get("current_speed_9"), "current_speed_9", record, errors, warnings
    )
    current_direction_9 = validators["decimal"](
        record.get("current_direction_9"),
        "current_direction_9",
        record,
        errors,
        warnings,
    )

    vel_e_cell_10 = validators["decimal"](
        record.get("vel_e_cell_10"), "vel_e_cell_10", record, errors, warnings
    )
    vel_n_cell_10 = validators["decimal"](
        record.get("vel_n_cell_10"), "vel_n_cell_10", record, errors, warnings
    )
    vel_u_cell_10 = validators["decimal"](
        record.get("vel_u_cell_10"), "vel_u_cell_10", record, errors, warnings
    )
    current_speed_10 = validators["decimal"](
        record.get("current_speed_10"), "current_speed_10", record, errors, warnings
    )
    current_direction_10 = validators["decimal"](
        record.get("current_direction_10"),
        "current_direction_10",
        record,
        errors,
        warnings,
    )

    payload = {
        "dataID": dataID,
        "eventID": eventID,
        "eventDate": time,
        "eventTime": record.get("eventTime"),
        "locationID": locationID,
        "underwater_par": underwater_par,
        "terrestrial_par": terrestrial_par,
        "exo_temperature": exo_temperature,
        "sp_cond": sp_cond,
        "salinity": salinity,
        "ph": ph,
        "odo_sat": odo_sat,
        "odo": odo,
        "aquadopp_temperature": aquadopp_temperature,
        "corrected_wind_direction": corrected_wind_direction,
        "corrected_wind_speed": corrected_wind_speed,
        "air_temperature": air_temperature,
        "relative_humidity": relative_humidity,
        "barometric_pressure": barometric_pressure,
        "precipitation_intensity": precipitation_intensity,
        "precipitation_total": precipitation_total,
        "wmo_average_wind_direction": wmo_average_wind_direction,
        "wmo_average_wind_speed": wmo_average_wind_speed,
        "latitude": latitude,
        "longitude": longitude,
        "vel_e_cell_1": vel_e_cell_1,
        "vel_n_cell_1": vel_n_cell_1,
        "vel_u_cell_1": vel_u_cell_1,
        "current_speed_1": current_speed_1,
        "current_direction_1": current_direction_1,
        "vel_e_cell_2": vel_e_cell_2,
        "vel_n_cell_2": vel_n_cell_2,
        "vel_u_cell_2": vel_u_cell_2,
        "current_speed_2": current_speed_2,
        "current_direction_2": current_direction_2,
        "vel_e_cell_3": vel_e_cell_3,
        "vel_n_cell_3": vel_n_cell_3,
        "vel_u_cell_3": vel_u_cell_3,
        "current_speed_3": current_speed_3,
        "current_direction_3": current_direction_3,
        "vel_e_cell_4": vel_e_cell_4,
        "vel_n_cell_4": vel_n_cell_4,
        "vel_u_cell_4": vel_u_cell_4,
        "current_speed_4": current_speed_4,
        "current_direction_4": current_direction_4,
        "vel_e_cell_5": vel_e_cell_5,
        "vel_n_cell_5": vel_n_cell_5,
        "vel_u_cell_5": vel_u_cell_5,
        "current_speed_5": current_speed_5,
        "current_direction_5": current_direction_5,
        "vel_e_cell_6": vel_e_cell_6,
        "vel_n_cell_6": vel_n_cell_6,
        "vel_u_cell_6": vel_u_cell_6,
        "current_speed_6": current_speed_6,
        "current_direction_6": current_direction_6,
        "vel_e_cell_7": vel_e_cell_7,
        "vel_n_cell_7": vel_n_cell_7,
        "vel_u_cell_7": vel_u_cell_7,
        "current_speed_7": current_speed_7,
        "current_direction_7": current_direction_7,
        "vel_e_cell_8": vel_e_cell_8,
        "vel_n_cell_8": vel_n_cell_8,
        "vel_u_cell_8": vel_u_cell_8,
        "current_speed_8": current_speed_8,
        "current_direction_8": current_direction_8,
        "vel_e_cell_9": vel_e_cell_9,
        "vel_n_cell_9": vel_n_cell_9,
        "vel_u_cell_9": vel_u_cell_9,
        "current_speed_9": current_speed_9,
        "current_direction_9": current_direction_9,
        "vel_e_cell_10": vel_e_cell_10,
        "vel_n_cell_10": vel_n_cell_10,
        "vel_u_cell_10": vel_u_cell_10,
        "current_speed_10": current_speed_10,
        "current_direction_10": current_direction_10,
        # 額外欄位：供既有視圖用
        "time": time,
    }

    return payload, errors, warnings
