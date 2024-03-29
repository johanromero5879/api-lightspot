from fastapi import Depends
from dependency_injector.wiring import Provide, inject

from app.common.domain import ValueId
from app.flash.domain import BaseFlash
from app.flash.application import GetFlashesRecord, InsertFlashes


@inject
async def process_flashes_record(
    raw_flashes: list[BaseFlash],
    countries: list[str],
    file: str | None = None,
    user_id: ValueId | None = None,
    get_flashes_record: GetFlashesRecord = Depends(Provide["services.get_flashes_record"]),
    insert_flashes: InsertFlashes = Depends(Provide["services.insert_flashes"])
):
    flashes = await get_flashes_record(
        raw_flashes=raw_flashes,
        countries=countries,
        file=file,
        user_id=user_id
    )  # Process the raw flashes and get a list of processed flashes

    if len(flashes) == 0:  # Check if there are any processed flashes
        raise ValueError("there is no flashes to process")

    await insert_flashes(flashes)

    return flashes
