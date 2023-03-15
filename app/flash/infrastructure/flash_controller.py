from fastapi import APIRouter, UploadFile, HTTPException, Depends, status, Security
from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError
from httpx import RequestError

from app.common.application import FileSizeConverter

from app.user.domain import UserOut

from app.auth.infrastructure import get_current_user
from app.role.domain import Permission

from app.flash.application import GetRawFlashes, GetFlashesRecord, InsertFlashes
from app.flash.infrastructure import FormatFileError, RecordsResult

router = APIRouter(
    prefix="/flashes",
    tags=["flashes"]
)

allowed_extensions = ["txt", "loc"]


@router.post(
    path="/upload",
    response_model=RecordsResult
)
@inject
async def upload_file(
    file: UploadFile,
    user: UserOut = Security(get_current_user, scopes=[Permission.UPLOAD_FLASHES_DATA]),
    get_raw_flashes: GetRawFlashes = Depends(Provide["services.get_raw_flashes"]),
    get_flashes_record: GetFlashesRecord = Depends(Provide["services.get_flashes_record"]),
    insert_flashes: InsertFlashes = Depends(Provide["services.insert_flashes"])
):
    """
    Handle the uploading of a file containing flash data.

    Parameters:
        file: A file to be uploaded containing flash data
        user: The authenticated user with the correct permissions.
        get_raw_flashes: A dependency to get raw flashes from the uploaded file.
        get_flashes_record: A dependency to process the raw flashes and get processed flashes.
        insert_flashes: A dependency to insert the processed flashes into the database.

    Returns:
        RecordsResult: The result of the upload process, containing the number of original and processed records
    """

    extension = file.filename.split(".")[-1]
    file_size_limit_megabytes = 3
    file_size_megabytes = FileSizeConverter.bytes_to_megabytes(file.size)

    if extension not in allowed_extensions:
        raise FormatFileError(f"file must have the following extensions: {allowed_extensions}")

    if file_size_megabytes > file_size_limit_megabytes:
        raise FormatFileError(f"file size must not be greater than {file_size_limit_megabytes} MB")

    try:
        content = await file.read()
        records = content.decode("utf-8").splitlines()
        raw_flashes = await get_raw_flashes(records)

        flashes = await get_flashes_record(
            raw_flashes=raw_flashes,
            countries=["co"],
            user_id=user.id
        )  # Process the raw flashes and get a list of processed flashes

        if len(flashes) == 0:  # Check if there are any processed flashes
            raise ValueError("there is no flashes to process")

        await insert_flashes(flashes)

        return RecordsResult(
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="there was an error uploading the file"
        )
    except RequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error on requesting coordinates to the geolocator api"
        )
    finally:
        file.file.close()
