from httpx import AsyncClient
from asyncio import gather

from app.common.domain import ValueId
from app.flash.domain import BaseFlash, FlashIn
from app.flash.application import ReverseGeocode


class GetFlashesRecord:
    def __init__(self, reverse_geocode: ReverseGeocode):
        self.reverse_geocode = reverse_geocode

    async def __call__(self,
                       raw_flashes: list[BaseFlash],
                       countries: list[str],
                       file: str | None = None,
                       user_id: ValueId | None = None
                       ) -> list[FlashIn]:
        """
        Processes a list of raw flash objects, filters the ones that match certain countries,
        and returns a list of flash objects.

        :param raw_flashes: A list of raw flash objects to process.
        :param countries: A list of country codes to filter the flashes by, given in ISO 3166-1 Alpha-2 code
        :param filename: An optional filename to identify a bunch of flashes.
        :param user_id: An optional user ID to assign to the records.

        :return: A list of FlashIn objects that match the specified countries.
        """
        flashes = []
        async with AsyncClient() as client:
            chunk_size = 10

            for index in range(0, len(raw_flashes), chunk_size):
                # Split the raw_flashes list into chunks of size chunk_size
                chunk = raw_flashes[index:index + chunk_size]

                # Create a list of coroutines to fetch flash data for each flash in the current chunk
                tasks = [self.get_flash_with_location(flash, file, user_id, client) for flash in chunk]

                # Wait for all the coroutines to finish and get their results
                results = await gather(*tasks)

                # Filter the results to include only the flashes that match the specified countries
                flashes.extend([
                    flash
                    for flash in results
                    if flash is not None and flash.location.country in countries
                ])

        return flashes

    async def get_flash_with_location(self,
                                      flash: BaseFlash,
                                      file: str | None,
                                      user_id: ValueId | None,
                                      client: AsyncClient) -> FlashIn | None:
        """
        Fetches a FlashIn object for the specified raw flash object and adds location and user data.

        :param flash: The raw flash object to fetch data for.
        :param file: An optional filename to identify a bunch of flashes.
        :param user_id: An optional user ID to include in the output.
        :param client: The httpx AsyncClient instance to use for making API requests.

        :return: A FlashIn object with location and user data, or None if no location data was found.
        """
        location = await self.reverse_geocode(flash.lat, flash.lon, client)

        if location:
            return FlashIn(
                **flash.dict(exclude_none=True),
                location=location,
                file=file,
                user=user_id
            )
