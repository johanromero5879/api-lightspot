from datetime import date as Date, time as Time, datetime, timedelta, timezone
import re


def date_to_datetime(
    date: Date,
    time: Time | str,
    utc_offset: str = "+00:00"
):
    if type(time) == str:
        if time == "min":
            time = datetime.min.time()
        else:
            time = datetime.max.time()

    date_time = datetime.combine(date, time)

    return apply_timezone(date_time, utc_offset)


def apply_timezone(date: datetime, utc_offset: str):
    offset = get_utc_offset_timedelta(utc_offset)
    return date.replace(tzinfo=timezone(offset))


def get_datetime_now(utc_offset: str | None = None):
    if not utc_offset:
        return datetime.now()

    offset = get_utc_offset_timedelta(utc_offset)
    tz = timezone(offset)

    return datetime.now(tz=tz)


def get_utc_offset_timedelta(utc_offset: str):
    # Set the timezone
    hours = int(utc_offset.split(":")[0])
    minutes = int(utc_offset.split(":")[1])

    return timedelta(hours=hours, minutes=minutes)


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
