from pydantic import BaseModel


class MostActivity(BaseModel):
    year: int | None
    month: str | None
    total: int = 0


class MostTimeOfDay(BaseModel):
    name: str
    total: int = 0


class Year(BaseModel):
    total: int = 0
    months: dict[str, int]


class TimeInsight(BaseModel):
    most_activity: MostActivity
    years: dict[str, Year]
    times_of_day: dict[str, int]
    most_time_of_day: MostTimeOfDay
    hours: dict[str, int]


class Insight(BaseModel):
    total: int = 0
    time: TimeInsight | None
    location: dict[str, int] | None

