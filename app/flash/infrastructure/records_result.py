from pydantic import BaseModel


class RecordsResult(BaseModel):
    read_file: str
    original_records: int
    processed_records: int
