from datetime import datetime
from dateutil import parser
import pytz
import re
from zoneinfo import ZoneInfo


def validate_integer(value, field_name, record):
    """
    檢查並嘗試將值轉換為整數。如果值為 None 或 'NA'，返回 None。
    如果轉換失敗，打印錯誤訓息並返回 None。
    """
    if value is None or value == "NA":
        return None  # 設為 None，以便存儲為 NULL
    else:
        try:
            return int(value)  # 嘗試將值轉換為整數
        except ValueError:
            print(
                f'    - ERROR: Invalid integer for {field_name}: {value} in record with dataID: {record.get("dataID")}'
            )
            return None  # 跳過無法轉換為整數的資料


def validate_date(value, field_name, record):
    """
    檢查並嘗試將值轉換為 YYYY-MM-DD 格式。如果值為 None 或 'NA'，返回 None。
    - 如果缺少日的格式：YYYY-MM（補該月第一天）
    - 其他：先嘗試 ISO 格式 (YYYY-MM-DD)，如果失敗，則嘗試其他常見格式。
    """
    if value is None or value == "NA":
        return None  # 設為 None，以便存儲為 NULL

    # 補上該月的第一天
    if re.match(r"^\d{4}-\d{2}$", value):
        try:
            time = datetime.strptime(f"{value}-01", "%Y-%m-%d").date()
            return time
        except ValueError:
            return None

    # 先嘗試 ISO 格式
    try:
        time = datetime.fromisoformat(value).date()
        return time
    except ValueError:
        pass  # ISO 格式解析失敗，繼續嘗試其他格式

    # 嘗試解析 ISO 8601 擴展格式（包含毫秒、時區等）
    try:
        parsed_date = parser.parse(value)
        return parsed_date.date()
    except ValueError:
        pass

    # 如果 ISO 格式失敗，嘗試自定義格式
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S"]  # 支援的日期格式
    for date_format in date_formats:
        try:
            time = datetime.strptime(value, date_format).date()
            return time
        except ValueError:
            continue  # 嘗試下一個日期格式

    # 如果無法匹配任何格式，打印錯誤並返回 None
    print(
        f'    - ERROR: Invalid date for {field_name}: {value} in record with dataID: {record.get("dataID")}'
    )
    return None


def validate_decimal(value, field_name, record):
    """
    檢查並嘗試將值轉換為浮點數，限制小數位數到8位。
    如果值為 None 或 'NA'，返回 None。
    如果轉換失敗，打印錯誤訓息並返回 None。
    """
    if value is None or value == "NA":
        return None  # 設為 None，以便存儲為 NULL
    else:
        try:
            # 嘗試將值轉換為浮點數並限制到 8 位小數
            return round(float(value), 8)
        except (ValueError, TypeError):
            print(
                f'    - ERROR: Invalid decimal for {field_name}: {value} in record with dataID: {record.get("dataID")}'
            )
            return None  # 跳過無法轉換為浮點數的資料


def validate_datetime(value, field_name, record):
    """
    檢查並嘗試將值轉換為帶有時區的 datetime 格式。
    如果值為 None 或 'NA'，返回 None。否則返回 UTC 時區的 datetime 物件。
    """
    if value is None or value == "NA":
        return None  # 設為 None，以便存儲為 NULL
    else:
        try:
            # 將 ISO 8601 格式的日期字串轉換為 datetime 物件
            dt = datetime.fromisoformat(value)

            # 假設原始時間沒有時區，這裡可以指定默認的時區，例如 UTC
            if dt.tzinfo is None:
                # 添加 UTC 時區
                dt = dt.replace(tzinfo=pytz.UTC)

            return dt
        except ValueError:
            print(
                f'    - ERROR: Invalid datetime for {field_name}: {value} in record with dataID: {record.get("dataID")}'
            )
            return None  # 跳過無法轉換為 datetime 的資料


def combine_datetime(date_value, time_value, record):
    """
    檢查跟轉換 date 跟 time，轉換成功過後，
    把 date 跟 time 合併成 datetime 格式，
    格式不符合則返回 None。
    """
    try:
        # 將字串轉換為 date 物件
        if isinstance(date_value, str):
            # 處理 ISO 格式（
            if "T" in date_value:
                date_value = datetime.fromisoformat(date_value).date()
            else:
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()

        # 將字串轉換為 time 物件
        if isinstance(time_value, str):
            if "+" in time_value:  # 處理有時區
                time_value = datetime.fromisoformat(f"2000-01-01T{time_value}").time()
            else:
                time_value = datetime.strptime(time_value, "%H:%M:%S").time()

        # 去掉 tzinfo
        if time_value.tzinfo:
            time_value = time_value.replace(tzinfo=None)

        dt = datetime.combine(date_value, time_value)
        dt = dt.replace(tzinfo=ZoneInfo("Asia/Taipei"))

        return dt
    except ValueError:
        print(
            f'    - ERROR: Invalid datetime for combined_datetime: {date_value}, {time_value} in record with dataID: {record.get("dataID")}'
        )
        return None
