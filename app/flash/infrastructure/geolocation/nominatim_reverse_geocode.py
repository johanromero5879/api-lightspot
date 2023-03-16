from httpx import AsyncClient

from app.flash.domain import Location
from app.flash.application import ReverseGeocode


class NominatimReverseGeocode(ReverseGeocode):
    ZOOM = 10  # city

    def __init__(self, api_uri: str):
        self.api_uri = api_uri

    async def __call__(self, lat: float, lon: float, client: AsyncClient) -> Location | None:
        response = await client.get(
            url=f"{self.api_uri}/reverse",
            params={
                "format": "jsonv2",
                "lat": lat,
                "lon": lon,
                "zoom": self.ZOOM
            }
        )

        location = response.json()

        if "address" in location:
            location = location["address"]

            return Location(
                country=location.get("country_code"),
                state=location.get("state") or location.get("region"),
                province=location.get("state_district"),
                city=location.get("county") or location.get("town") or location.get("city")
            )
