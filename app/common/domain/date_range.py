from datetime import date, datetime

from pydantic import BaseModel


class DateRange(BaseModel):
    start_date: date
    end_date: date


class DatetimeRange(BaseModel):
    start_date: datetime
    end_date: datetime
