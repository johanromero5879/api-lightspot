import datetime
import re


def date_to_datetime(
    date: datetime.date,
    time: datetime.time | str,
    utc_offset: str = "+00:00"
):
    if type(time) == str:
        if time == "min":
            time = datetime.datetime.min.time()
        else:
            time = datetime.datetime.max.time()

    hours = int(utc_offset.split(":")[0])
    offset = datetime.timedelta(hours=hours)
    tz = datetime.timezone(offset)

    return datetime.datetime.combine(date, time, tz)


def add_sign_to_utc_offset(offset: str) -> str:
    if not re.match(r"^[-+]", offset):
        offset = f"+{offset.strip()}"

    return offset


def is_valid_utc_offset(offset: str):
    pattern = r'^([-+]\d{2}):(\d{2})$'
    match = re.match(pattern, offset)

    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))

        if hours < -12 or hours > 14:
            return False

        if minutes not in [0, 30, 45]:
            return False

        if minutes == 45 and hours not in [5, 8, 12]:
            return False

        if minutes == 30 and hours not in [-9, -3, 3, 4, 5, 6, 9, 10]:
            return False

        return True

    return False
