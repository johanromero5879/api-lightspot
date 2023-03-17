from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, Security
from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from httpx import RequestError

from app.common.domain import DateRange
from app.common.application import FileSizeConverter

from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user, verify_device_address
from app.role.domain import Permission

from app.flash.domain import Location, FlashQuery, BaseFlash
from app.flash.application import GetRawFlashes, FindFlashesBy
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
        file: A file to be uploaded containing flash data
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

        flashes = await process_flashes_record(raw_flashes, user.id)

        return FileRecordsResult(
            read_file=file.filename,
            original_records=len(raw_flashes),
            processed_records=len(flashes)
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.errors()
        )
    except ValueError:
        raise UploadFileError()
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

        flashes = await process_flashes_record(raw_flashes)

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
    path="/"
)
@inject
async def filter_flashes(
    date_range: DateRange = Depends(),
    location: Location = Depends(),
    find_flashes_by: FindFlashesBy = Depends(Provide["services.find_flashes_by"])
):
    try:
        query = FlashQuery(
            date_range=date_range,
            location=location
        )

        flashes = await find_flashes_by(query)

        return flashes
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
