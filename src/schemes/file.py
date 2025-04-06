import datetime
from uuid import UUID
from pydantic import BaseModel


class AddFileDTO(BaseModel):
    filename: str | None
    bucket_name: str
    size: int | None


class EditFileDTO(BaseModel):
    filename: str | None = None
    bucket_name: str | None = None
    size: int | None = None


class OutputFileDTO(BaseModel):
    id: UUID
    filename: str | None
    bucket_name: str
    size: int | None
    created_at: datetime.datetime

    class Config:
        from_attributes = True
