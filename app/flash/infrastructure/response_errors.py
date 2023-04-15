from fastapi import HTTPException, status


class FormatFileError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class UploadFileError(HTTPException):
    def __init__(self, detail: str | None = None):
        if not detail:
            detail = "there was an error uploading the file"

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class GeocodeApiError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="error on requesting coordinates to the geolocator api"
        )
