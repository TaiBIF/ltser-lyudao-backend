from django.conf import settings
import requests
from datetime import datetime
import pytz
import numpy as np

# API 認證資訊
API_CONFIG = {
    "APIKey": settings.WQDATA_API_KEY,
}

# 查詢條件
QUERY_PARAMS = {
    "GG": {
        "site": 3964,
        "params": {
            "parameterIds": "100416,100415,100414,100418,100417,100333,100340,100335,100337,100336,100352,100353,100358,100359,100364,100365,100370,100371,100376,100377,100382,100383,100389,100394,100395,100400,100401,100406,100407"
        },
    },
    "GW": {
        "site": 3965,
        "params": {
            "parameterIds": "100543,100542,100541,100545,100544,100460,100467,100462,100464,100463,100479,100480,100485,100486,100491,100492,100497,100503,100504,100509,100510,100515,100516,100516,100521,100527,100528,100533,100534"
        },
    },
}

WIND_DIRECTIONS_16 = [
    ("北", "N"),
    ("北北東", "NNE"),
    ("東北", "NE"),
    ("東北東", "ENE"),
    ("東", "E"),
    ("東南東", "ESE"),
    ("東南", "SE"),
    ("南南東", "SSE"),
    ("南", "S"),
    ("南南西", "SSW"),
    ("西南", "SW"),
    ("西南西", "WSW"),
    ("西", "W"),
    ("西北西", "WNW"),
    ("西北", "NW"),
    ("北北西", "NNW"),
]

LAYER_MAP = {
    1: "2.8",
    2: "7.8",
    3: "12.8",
    4: "17.8",
    5: "22.8",
    6: "27.8",
    7: "32.8",
    8: "37.8",
    9: "42.8",
    10: "47.8",
}


def get_latest_device_data(device_id, api_key, query_params=None):
    """查詢指定設備的最新參數資料"""
    url = (
        f"https://www.wqdatalive.com/api/v1/devices/{device_id}/parameters/data/latest"
    )
    params = {"apiKey": api_key}
    if query_params:
        params.update(query_params)

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("data", [])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def degrees_to_16_wind_direction_label(degrees):
    index = int((float(degrees) + 11.25) % 360 // 22.5)
    zh_TW, en = WIND_DIRECTIONS_16[index]
    return f"{zh_TW}（{en}）"


def transform_device_data(data_list):
    """將 API 回傳資料轉換成字典，時間轉成東八區"""
    result = {}
    utc = pytz.utc
    taipei_tz = pytz.timezone("Asia/Taipei")

    for item in data_list:
        name = item.get("name")
        timestamp_str = item.get("timestamp")
        value = item.get("value")

        # 轉換時間字串成 datetime，再轉成東八區
        try:
            dt_utc = utc.localize(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
            dt_taipei = dt_utc.astimezone(taipei_tz)
            timestamp_local = dt_taipei.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            timestamp_local = None

        entry = {"timestamp": timestamp_local, "value": value}

        # 轉換風向角度，存在 direction 中
        if name == "Corrected Wind Direction":
            direction_label = degrees_to_16_wind_direction_label(float(value))
            entry["direction"] = direction_label

        result[name] = entry
    return result


def calcaulate_current_speed_and_direction(data_dict):
    """用東、北分量計算流速、流向，並直接合併進 data_dict 中"""
    for i in range(1, 11):
        vel_e_key = f"Vel.E (Cell {i})"
        vel_n_key = f"Vel.N (Cell {i})"
        new_key = LAYER_MAP.get(i)

        if vel_e_key in data_dict and vel_n_key in data_dict:
            try:
                vel_e = float(data_dict[vel_e_key]["value"])
                vel_n = float(data_dict[vel_n_key]["value"])
                timestamp = data_dict[vel_e_key]["timestamp"]

                # 計算流速（m/s）
                speed = float(np.sqrt(vel_e**2 + vel_n**2)) / 1000

                # 計算流速（節）
                speed_knot = speed * 1.94384

                # 計算流向角度
                direction_degree = float(
                    (np.degrees(np.arctan2(vel_e, vel_n)) + 360) % 360
                )

                # 轉換為 16 方位
                direction = degrees_to_16_wind_direction_label(direction_degree)

                # 合併進原始字典
                data_dict[new_key] = {
                    "speed": float(round(speed, 2)),
                    "speed_knot": float(round(speed_knot, 2)),
                    "direction_degrees": float(round(direction_degree, 1)),
                    "direction": direction,
                    "timestamp": timestamp,
                }
            except Exception as e:
                data_dict[new_key] = {"error": str(e)}
    return data_dict
