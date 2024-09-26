from datetime import datetime
import pytz

def validate_integer(value, field_name, record):
    """
    檢查並嘗試將值轉換為整數。如果值為 None 或 'NA'，返回 None。
    如果轉換失敗，打印錯誤訓息並返回 None。
    """
    if value is None or value == 'NA':
        return None  # 設為 None，以便存儲為 NULL
    else:
        try:
            return int(value)  # 嘗試將值轉換為整數
        except ValueError:
            print(f'    - ERROR: Invalid integer for {field_name}: {value} in record with dataID: {record.get("dataID")}')
            return None  # 跳過無法轉換為整數的資料

def validate_date(value, field_name, record):
    """
    檢查並嘗試將值轉換為 YYYY-MM-DD 格式。如果值為 None 或 'NA'，返回 None。
    先嘗試 ISO 格式 (YYYY-MM-DD)，如果失敗，則嘗試其他常見格式。
    """
    if value is None or value == 'NA':
        return None  # 設為 None，以便存儲為 NULL
    else:
        # 先嘗試 ISO 格式
        try:
            time = datetime.fromisoformat(value).date()
            return time
        except ValueError:
            pass  # ISO 格式解析失敗，繼續嘗試其他格式

        # 如果 ISO 格式失敗，嘗試自定義格式
        date_formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y-%m-%dT%H:%M:%S']  # 支援的日期格式
        for date_format in date_formats:
            try:
                time = datetime.strptime(value, date_format).date()
                return time
            except ValueError:
                continue  # 嘗試下一個日期格式

        # 如果無法匹配任何格式，打印錯誤並返回 None
        print(f'    - ERROR: Invalid date for {field_name}: {value} in record with dataID: {record.get("dataID")}')
        return None

def validate_decimal(value, field_name, record):
    """
    檢查並嘗試將值轉換為浮點數，限制小數位數到8位。
    如果值為 None 或 'NA'，返回 None。
    如果轉換失敗，打印錯誤訓息並返回 None。
    """
    if value is None or value == 'NA':
        return None  # 設為 None，以便存儲為 NULL
    else:
        try:
            # 嘗試將值轉換為浮點數並限制到 8 位小數
            return round(float(value), 8)
        except (ValueError, TypeError):
            print(f'    - ERROR: Invalid decimal for {field_name}: {value} in record with dataID: {record.get("dataID")}')
            return None  # 跳過無法轉換為浮點數的資料

def validate_datetime(value, field_name, record):
    """
    檢查並嘗試將值轉換為帶有時區的 datetime 格式。
    如果值為 None 或 'NA'，返回 None。否則返回 UTC 時區的 datetime 物件。
    """
    if value is None or value == 'NA':
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
            print(f'    - ERROR: Invalid datetime for {field_name}: {value} in record with dataID: {record.get("dataID")}')
            return None  # 跳過無法轉換為 datetime 的資料