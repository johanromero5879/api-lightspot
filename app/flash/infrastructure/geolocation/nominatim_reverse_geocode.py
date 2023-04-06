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

            location = Location(
                country=location.get("country_code"),
                state=location.get("state") or location.get("region"),
                city=location.get("county") or location.get("town") or location.get("city") or location.get("locality")
                or location.get("village") or location.get("hamlet")
            )

            return self.clean_location(location)

    def clean_location(self, location: Location) -> Location:
        if location.country:
            location.country = location.country.upper()

        if location.state and not location.state.__contains__("RAP"):
            location.state = location.state.replace(".", "").strip()
        else:
            location.state = None

        if location.city:
            location.city = location.city.replace(".", "").strip()

            if location.city.__contains__("-"):
                location.city = location.city.split("-")[-1].strip()

        return location
