from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, Security
from dependency_injector.wiring import Provide, inject
from httpx import RequestError

from app.common.domain import DateRange
from app.common.application import FileSizeConverter, is_valid_utc_offset, add_sign_to_utc_offset, date_to_datetime

from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user, verify_device_address
from app.role.domain import Permission

from app.flash.domain import Location, FlashQuery, BaseFlash, Insight, FlashOut
from app.flash.application import GetRawFlashes, FindFlashesBy, GetInsights, FlashesNotFoundError
from app.flash.infrastructure import FormatFileError, GeocodeApiError, UploadFileError, RecordsResult, \
    process_flashes_record, FileRecordsResult

router = APIRouter(
    prefix="/flashes",
    tags=["flashes"]
)

ALLOWED_EXTENSIONS = ["txt", "loc"]


@router.post(
    path="/upload",
    response_model=FileRecordsResult
)
@inject
async def upload_file(
    file: UploadFile,
    user: UserOut = Security(get_current_user, scopes=[Permission.UPLOAD_FLASHES_DATA]),
    get_raw_flashes: GetRawFlashes = Depends(Provide["services.get_raw_flashes"])
):
    """
    Handle the uploading of a file containing flash data.

    Parameters:
        file: A file to be uploaded containing flash data.
        user: The authenticated user with the correct permissions.
        get_raw_flashes: A dependency to get raw flashes from the uploaded file.

    Returns:
        RecordsResult: The result of the upload process, containing the number of original and processed records
    """

    extension = file.filename.split(".")[-1]
    file_size_limit_megabytes = 3
    file_size_megabytes = FileSizeConverter.bytes_to_megabytes(file.size)

    if extension not in ALLOWED_EXTENSIONS:
        raise FormatFileError(f"file must have the following extensions: {ALLOWED_EXTENSIONS}")

    if file_size_megabytes > file_size_limit_megabytes:
        raise FormatFileError(f"file size must not be greater than {file_size_limit_megabytes} MB")

    try:
        content = await file.read()
        records = content.decode("utf-8").splitlines()
        raw_flashes = await get_raw_flashes(records)

        countries = ["CO"]
        flashes = await process_flashes_record(raw_flashes, countries, user.id)

        return FileRecordsResult(
            read_file=file.filename,
            original_records=len(raw_flashes),
            processed_records=len(flashes)
        )
    except ValueError as error:
        raise UploadFileError(str(error))
    except RequestError:
        raise GeocodeApiError()
    finally:
        file.file.close()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_device_address)],
    response_model=RecordsResult
)
@inject
async def register_flashes(
    raw_flashes: list[BaseFlash]
):
    try:
        if len(raw_flashes) == 0:
            raise ValueError("there must be at least one record in raw_flashes")

        countries = ["CO"]
        flashes = await process_flashes_record(raw_flashes, countries)

        return RecordsResult(
            original_records=len(raw_flashes),
            processed_records=len(flashes)
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except RequestError:
        raise GeocodeApiError()


@router.get(
    path="/",
    response_model=list[FlashOut]
)
@inject
async def filter_flashes(
    utc_offset: str = "+00:00",
    date_range: DateRange = Depends(),
    location: Location = Depends(),
    find_flashes_by: FindFlashesBy = Depends(Provide["services.find_flashes_by"])
):
    try:
        query = get_query(location, date_range, utc_offset)

        flashes = await find_flashes_by(query, utc_offset)

        return flashes
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get(
    path="/insights",
    response_model=Insight
)
@inject
async def insights(
    utc_offset: str = "+00:00",
    date_range: DateRange = Depends(),
    location: Location = Depends(),
    get_insights: GetInsights = Depends(Provide["services.get_insights"])
):
    try:
        query = get_query(location, date_range, utc_offset)

        result = await get_insights(query, utc_offset)

        return result
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    except FlashesNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


def get_query(
    location: Location,
    date_range: DateRange,
    utc_offset: str
) -> FlashQuery:
    utc_offset = add_sign_to_utc_offset(utc_offset)

    if not location.state and not location.city:
        raise ValueError("state or city are required")

    if not is_valid_utc_offset(utc_offset):
        raise ValueError(f"utc offset '{utc_offset}' not valid")

    query = FlashQuery(
        date_range=date_range,
        location=location
    )

    return format_query(query, utc_offset)


def format_query(query: FlashQuery, utc_offset: str) -> FlashQuery:
    query.location.country = query.location.country.upper()

    query.date_range.start_date = date_to_datetime(query.date_range.start_date, "min", utc_offset)
    query.date_range.end_date = date_to_datetime(query.date_range.end_date, "max", utc_offset)

    return query
