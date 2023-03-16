from datetime import datetime

from pydantic import Field

from app.common.domain import Entity, ValueId, DateRange


class Location(Entity):
    country: str
    state: str | None
    province: str | None
    city: str | None


class BaseFlash(Entity):
    occurrence_date: datetime
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    residual_fit_error: float = Field(ge=0, le=30)
    stations: int = Field(ge=5)


class FlashIn(BaseFlash):
    location: Location
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: ValueId | None = None


class FlashOut(BaseFlash):
    location: Location
    id: ValueId = Field(alias="_id")


class FlashQuery(Entity):
    date_range: DateRange
    location: Location
