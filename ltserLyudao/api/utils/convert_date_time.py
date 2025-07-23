from datetime import datetime
import pytz


def parse_time_str(time_str):
    """解析 HH:MM[:SS] 時間字串成 datetime.time 物件"""
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError("Invalid time format. Expected HH:MM or HH:MM:SS")


def combine_local_to_utc(date_str, time_str, tz, is_end=False):
    """將本地日期與時間轉換為 UTC datetime"""
    base_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if time_str:
        t = parse_time_str(time_str)
    else:
        t = datetime.max.time() if is_end else datetime.min.time()

    local_dt = tz.localize(datetime.combine(base_date, t))
    return local_dt.astimezone(pytz.UTC)


def convert_time_only_to_utc_time(t_str, tz):
    """將本地時間字串轉換為 UTC 的時間部分（忽略日期）"""
    local_time = parse_time_str(t_str)
    dummy_date = datetime(
        1996, 11, 26, local_time.hour, local_time.minute, local_time.second
    )
    local_dt = tz.localize(dummy_date)
    utc_dt = local_dt.astimezone(pytz.UTC)
    return utc_dt.time()
