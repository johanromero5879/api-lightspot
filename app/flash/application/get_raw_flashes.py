from datetime import datetime

from app.flash.domain import BaseFlash


class GetRawFlashes:
    async def __call__(self, records: list[str]) -> list[BaseFlash]:
        """
        Parses a list of string records into a list of BaseFlash objects.

        :param records: A list of string records to parse.

        :return: A list of BaseFlash objects parsed from the input records.
        """
        flashes = []

        for record in records:
            date, time, lat, lon, resid, stations = record.split(",")

            flash = BaseFlash(
                occurrence_date=datetime.strptime(f'{date} {time}', '%Y/%m/%d %H:%M:%S.%f'),
                lat=float(lat),
                lon=float(lon),
                residual_fit_error=float(resid),
                stations=int(stations)
            )

            flashes.append(flash)

        return flashes
