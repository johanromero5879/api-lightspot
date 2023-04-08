from datetime import datetime

from app.flash.domain import BaseFlash, FLASH_DATE_FORMAT


class GetRawFlashes:
    async def __call__(self, records: list[str]) -> list[BaseFlash]:
        """
        Parses a list of string records into a list of BaseFlash objects.

        :param records: A list of string records to parse.

        :return: A list of BaseFlash objects parsed from the input records.
        """
        flashes = []

        for index, record in enumerate(records):
            try:
                date, time, lat, lon, resid, stations = record.split(",")

                date = date.strip()
                if date[0] == "\ufeff":
                    date = date[1:]

                time = time.strip()
                flash = BaseFlash(
                    occurrence_date=datetime.strptime(f'{date} {time}', FLASH_DATE_FORMAT),
                    lat=float(lat),
                    lon=float(lon),
                    residual_fit_error=float(resid),
                    stations=int(stations)
                )
                flashes.append(flash)
            except ValueError:
                raise ValueError(f"error on line {index + 1}: {record}")

        return flashes
