from pydantic import BaseModel


class MostActivity(BaseModel):
    year: int | None
    month: str | None
    total: int = 0


class MostPeriodOfDay(BaseModel):
    name: str
    total: int = 0


class Year(BaseModel):
    total: int = 0
    months: dict[str, int]


class TimeInsight(BaseModel):
    most_activity: MostActivity
    years: dict[str, Year]
    periods_of_day: dict[str, int]
    most_period_of_day: MostPeriodOfDay
    hours: dict[str, int]


class Insight(BaseModel):
    total: int = 0
    time: TimeInsight | None
    location: dict[str, int] | None

