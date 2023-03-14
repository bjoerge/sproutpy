from datetime import datetime, timezone, timedelta

utc = timezone(timedelta(0))


def json_datetime(year: int, month: int, day: int, hour: int, minute: int, second: int):
    return datetime(year, month, day, hour, minute, second, tzinfo=utc).isoformat()
