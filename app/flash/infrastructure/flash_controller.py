from datetime import datetime

from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, Security
from fastapi.responses import StreamingResponse
from dependency_injector.wiring import Provide, inject
from httpx import RequestError

from app.common.domain import DateRange
from app.common.application import FileSizeConverter, is_valid_utc_offset, add_sign_to_utc_offset, date_to_datetime

from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user, verify_device_address
from app.role.domain import Permission

from app.flash.domain import Location, FlashQuery, BaseFlash, Insight, FlashOut
from app.flash.application import GetRawFlashes, FindFlashesBy, GetInsights, FlashesNotFoundError, \
    generate_flash_report, FindFlashesByUser, RemoveFlashesLastDay, ExistsFile
from app.flash.infrastructure import FormatFileError, GeocodeApiError, UploadFileError, RecordsResult, \
    process_flashes_record, FileRecordsResult

router = APIRouter(
    prefix="/flashes",
    tags=["flashes"]
)

ALLOWED_EXTENSIONS = ["txt", "loc", "csv"]


@router.post(
    path="/upload",
    response_model=FileRecordsResult
)
@inject
async def upload_file(
    file: UploadFile,
    user: UserOut = Security(get_current_user, scopes=[Permission.UPLOAD_FLASHES_DATA]),
    exists_flashes_file: ExistsFile = Depends(Provide["services.exists_flashes_file"]),
    get_raw_flashes: GetRawFlashes = Depends(Provide["services.get_raw_flashes"])
):
    """
    Handle the uploading of a file containing flash data.

    Parameters:
        file: A file to be uploaded containing flash data.
        user: The authenticated user with the correct permissions.
        exists_flashes_file: A dependency to check if a filename was used before.
        get_raw_flashes: A dependency to get raw flashes from the uploaded file.

    Returns:
        RecordsResult: The result of the upload process, containing the number of original and processed records
    """

    extension = file.filename.split(".")[-1]
    filename = file.filename
    file_size_limit_megabytes = 7
    file_size_megabytes = FileSizeConverter.bytes_to_megabytes(file.size)

    if extension not in ALLOWED_EXTENSIONS:
        raise FormatFileError(f"file must have the following extensions: {ALLOWED_EXTENSIONS}")

    if file_size_megabytes > file_size_limit_megabytes:
        raise FormatFileError(f"file size must not be greater than {file_size_limit_megabytes} MB")

    try:
        exists_filename = await exists_flashes_file(filename)

        if exists_filename:
            raise ValueError(f"File {filename} was already uploaded")

        content = await file.read()
        records = content.decode("utf-8").splitlines()
        raw_flashes = await get_raw_flashes(records)

        countries = ["CO"]
        flashes = await process_flashes_record(raw_flashes, countries, filename, user.id)

        return FileRecordsResult(
            read_file=filename,
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


@router.get(
    path="/reports",
    dependencies=[
        Security(get_current_user, scopes=[Permission.GENERATE_FLASHES_REPORT])
    ]
)
@inject
async def reports(
    utc_offset: str = "+00:00",
    date_range: DateRange = Depends(),
    location: Location = Depends(),
    find_flashes_by: FindFlashesBy = Depends(Provide["services.find_flashes_by"])
):
    try:
        query = get_query(location, date_range, utc_offset)

        flashes = await find_flashes_by(query, utc_offset)
        if len(flashes) == 0:
            raise FlashesNotFoundError()

        # Generate the PDF report data
        pdf_name = f"{datetime.utcnow()}.pdf"
        pdf_data = await generate_flash_report(flashes, query, utc_offset)

        # Define a generator function to stream the PDF data
        def pdf_stream():
            yield pdf_data

        # Set the response headers
        headers = {
            "Content-Disposition": f"attachment; filename={pdf_name}",
            "Content-Type": "application/pdf"
        }

        # Return the PDF data as a streaming response
        return StreamingResponse(pdf_stream(), headers=headers)
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


@router.get(
    path="/{time_period}"
)
@inject
async def get_flashes_by_user(
    time_period: str,
    user: UserOut = Depends(get_current_user),
    find_flashes_by_user: FindFlashesByUser = Depends(Provide["services.find_flashes_by_user"])
):
    """
    This endpoint retrieves all flashes uploaded by the authenticated user within a specific time period

    Parameters:
        time_period: The time period to search for flashes, specified as a string
        with one of the following values:
            - week: Retrieve all flashes uploaded within the last 7 days.
            - day: Retrieve all flashes uploaded within the last 24 hours.
            - hour: Retrieve all flashes uploaded within the last hour.
        user: The authenticated user with the correct permissions.
        find_flashes_by_user: A dependency injection that provides the find_flashes_by_user service.

    Returns:
        A list of FlashOut object.
    """
    try:
        if time_period not in ["week", "day", "hour", "minute"]:
            raise ValueError("Time period not valid")

        time_period = f"1 {time_period}s"

        flashes = await find_flashes_by_user(
            user_id=user.id,
            period=time_period
        )

        return flashes
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete(
    path="/last-day",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def delete_flashes_last_day(
    file: str | None = None,
    user: UserOut = Security(get_current_user, scopes=[Permission.REMOVE_MY_UPLOADED_FLASHES]),
    remove_flashes_last_day: RemoveFlashesLastDay = Depends(Provide["services.remove_flashes_last_day"])
):
    """
    This endpoint deletes all flashes uploaded by the authenticated user within the last hour.
    """
    deleted = await remove_flashes_last_day(user_id=user.id, file=file)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No flashes to delete"
        )
