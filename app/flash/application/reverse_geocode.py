from abc import ABC, abstractmethod

from app.flash.domain import Location


class ReverseGeocode(ABC):
    @abstractmethod
    async def __call__(self, lat: float, lon: float, client) -> Location | None:
        """
        Reverse geocodes the given latitude and longitude using the specified client.

        :param lat: The latitude of the location to reverse geocode.
        :param lon: The longitude of the location to reverse geocode.
        :param client: The HTTP client to use for making the reverse geocoding request.

        :return: A Location object containing information about the reverse geocoded location,
        or None if the location could not be reverse geocoded.
        """
        pass
