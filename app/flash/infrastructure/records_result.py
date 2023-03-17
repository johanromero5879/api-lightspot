from pydantic import BaseModel


class RecordsResult(BaseModel):
    original_records: int
    processed_records: int


class FileRecordsResult(RecordsResult):
    read_file: str
