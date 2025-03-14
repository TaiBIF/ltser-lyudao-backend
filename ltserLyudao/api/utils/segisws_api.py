from django.conf import settings
import requests
import xml.etree.ElementTree as ET
import json

# API 端點
URL = "https://segisws.moi.gov.tw/STATWSSTData/AdminService.asmx"

# API 認證資訊
API_CONFIG = {
    "oAPPId": settings.SEGISWS_API_ID,
    "oAPIKey": settings.SEGISWS_API_KEY,
    "oResultDataType": "JSON",  # 回應格式
}

# 查詢條件
QUERY_PARAMS = {
    "oFilterCountys": "10014",  # 台東縣
    "oFilterTowns": "10014110",  # 綠島鄉
    "oFilterVillages": "*",
}

API_MAPPING = {
    "village": {
        "unit_code": "U01VI",
        "api_name": "GetVillageSTData",
        "id_field": "V_ID",
        "filter_village": f"<oFilterVillages>{QUERY_PARAMS['oFilterVillages']}</oFilterVillages>",
    },
    "town": {
        "unit_code": "U01TO",
        "api_name": "GetTownSTData",
        "id_field": "TOWN_ID",
        "filter_village": "",  # 鄉鎮級查詢不需要村里篩選
    }
}

THEME_MAPPING = {
    "summary": {
        "meta_code": "3A1FA_A1C1",
        "columns": "INFO_TIME,{id_field},H_CNT,P_CNT"
    },
    "index": {
        "meta_code": "3A1FA_A1C3",
        "columns": "INFO_TIME,{id_field},M_F_RAT,DEPENDENCY_RAT,A65_A0A14_RAT"
    },
    "dynamics": {
        "meta_code": "3A1FA_A1B34",
        "columns": "INFO_TIME,{id_field},NATURE_INC_CNT,SOCIAL_INC_CNT"
    },
    "pyramid": {
         "meta_code": "3A1FA_A1C5",
         "columns": "*"
    }
}

def send_soap_request(action, body):
    """發送 SOAP 請求"""
    soap_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            {body}
        </soap:Body>
    </soap:Envelope>"""

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"http://tempuri.org/{action}"
    }

    try:
        response = requests.post(URL, data=soap_request, headers=headers)
        response.raise_for_status()  # 如果請求失敗，會拋出 HTTPError
        return response.text
    except requests.RequestException as e:
        print(f"API 呼叫失敗：{e}")
        return None

def parse_soap_response(response_text, result_tag):
    """解析 SOAP 回應，提取 JSON 內容"""
    try:
        root = ET.fromstring(response_text)
        json_text = root.find(f".//{{http://tempuri.org/}}{result_tag}").text
        return json.loads(json_text)
    except (ET.ParseError, AttributeError, json.JSONDecodeError) as e:
        print(f"回應解析失敗：{e}")
        return None

def get_latest_time_list(level, query_type="summary"):
    """
    獲取最新的資料時間清單

    參數:
        level: "village" 表示村里, "town" 表示鄉鎮
        query_type: "summary" 表示人口統計, "index" 表示人口指標, "dynamics" 表示人口消長, "pyramid"表示人口結構
    
    回傳:
        最新時間列表（格式為 113Y12M 或 113Y4S）
    """

    api_info = API_MAPPING[level]

    if query_type not in THEME_MAPPING:
        raise ValueError("query_type 必須是 'summary','index','dynamics' 或 'pyramid'")
    
    meta_code = THEME_MAPPING[query_type]['meta_code']

    body = f"""
    <GetSTTimeList xmlns="http://tempuri.org/">
        <oAPPId>{API_CONFIG["oAPPId"]}</oAPPId>
        <oAPIKey>{API_CONFIG["oAPIKey"]}</oAPIKey>
        <oResultDataType>{API_CONFIG["oResultDataType"]}</oResultDataType>
        <oSTUnitCode>{api_info['unit_code']}</oSTUnitCode>
        <oMetaDatCode>{meta_code}</oMetaDatCode>
    </GetSTTimeList>
    """
    response_text = send_soap_request("GetSTTimeList", body)
    if not response_text:
        return []

    json_data = parse_soap_response(response_text, "GetSTTimeListResult")
    if not json_data or "DateList" not in json_data:
        return []

    date_list = [item["INFO_TIME"] for item in json_data["DateList"]]

    time_dict = {}
    for date in date_list:
        date = date.replace("Y", " ").replace("M", "").replace("S", "")
        date_parts = date.split()

        if query_type == "dynamics": # 只有人口消長是用季度計算
            if len(date_parts) == 2:
                year, quarter = map(int, date_parts)
            else:
                year = int(date_parts[0])
                quarter = 1  # 預設為第一季度
            time_dict[year] = max(time_dict.get(year, 0), quarter)
        else:
            if len(date_parts) == 2:
                year, month = map(int, date_parts)
                time_dict[year] = max(time_dict.get(year, 0), month)

    if query_type == "dynamics":
        return [f"{year}Y{quarter}S" for year, quarter in sorted(time_dict.items())]
    else:
        return [f"{year}Y{str(month).zfill(2)}M" for year, month in sorted(time_dict.items())]

def get_population_data(level, latest_dates, query_type="summary"):
    """
    查詢人口統計數據或人口統計指標
    
    參數:
        level: "village" 表示村里, "town" 表示鄉鎮
        latest_dates: 需要查詢的最新時間列表
        query_type: "summary" 表示人口統計, "index" 表示人口指標, "dynamics" 表示人口消長, "pyramid"表示人口結構
    """

    if not latest_dates:
        print("無可用的資料時間")
        return []

    api_info = API_MAPPING[level]

    if query_type not in THEME_MAPPING:
        raise ValueError("query_type 必須是 'summary','index','dynamics' 或 'pyramid'")

    selected_columns = THEME_MAPPING[query_type]['columns'].format(id_field=api_info["id_field"])

    body = f"""
    <{api_info['api_name']} xmlns="http://tempuri.org/">
        <oAPPId>{API_CONFIG["oAPPId"]}</oAPPId>
        <oAPIKey>{API_CONFIG["oAPIKey"]}</oAPIKey>
        <oSTUnitCode>{api_info["unit_code"]}</oSTUnitCode>
        <oMetaDatCode>{THEME_MAPPING[query_type]['meta_code']}</oMetaDatCode>
        <oSelectColumns>{selected_columns}</oSelectColumns>
        <oFilterSTTimes>{','.join(latest_dates)}</oFilterSTTimes>
        <oFilterCountys>{QUERY_PARAMS["oFilterCountys"]}</oFilterCountys>
        <oFilterTowns>{QUERY_PARAMS["oFilterTowns"]}</oFilterTowns>
        {api_info["filter_village"]}
        <oResultDataType>{API_CONFIG["oResultDataType"]}</oResultDataType>
    </{api_info['api_name']}>
    """

    response_text = send_soap_request(api_info["api_name"], body)
    if not response_text:
        return []

    json_data = parse_soap_response(response_text, f"{api_info['api_name']}Result")
    return json_data.get("RowDataList", [])

