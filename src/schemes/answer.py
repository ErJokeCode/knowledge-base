import datetime
import logging
from uuid import UUID
from pydantic import BaseModel, field_validator

_log = logging.getLogger(__name__)


class InputAnswerDTO(BaseModel):
    id_question: UUID
    answer: str
    links: list[str] | None = None
    tag_ids: list[UUID] | None = None


class AddAnswerDTO(BaseModel):
    id_question: UUID
    answer: str


class EditAnswerDTO(BaseModel):
    id_question: UUID | None = None
    answer: str | None = None


class OutputAnswerDTO(BaseModel):
    id: UUID
    id_question: UUID
    answer: str
    rating: float
    created_at: datetime.datetime

    links: list["LinkDTO"] | None
    answer_tags: list["TagDTO"]
    files: list["FileDTO"]

    @field_validator('answer_tags', mode='before')
    @classmethod
    def transform_tags(cls, v):
        if not v:
            return []

        if all(hasattr(item, 'tag') for item in v):
            return [item.tag for item in v]

        if all(isinstance(item, dict) and 'tag' in item for item in v):
            return [item['tag'] for item in v]

        return v

    @field_validator('files', mode='before')
    @classmethod
    def transform_files(cls, v):
        if not v:
            return []

        if all(hasattr(item, 'file') for item in v):
            return [item.file for item in v]

        if all(isinstance(item, dict) and 'file' in item for item in v):
            return [item['file'] for item in v]

        return v

    class Config:
        from_attributes = True


class TagAnswerDTO(BaseModel):
    tag: "TagDTO"

    class Config:
        from_attributes = True


class LinkDTO(BaseModel):
    id: UUID
    link: str

    class Config:
        from_attributes = True


class FileDTO(BaseModel):
    id: UUID
    filename: str | None
    size: int | None
    created_at: datetime.datetime

    file_tags: list["TagDTO"]

    @field_validator('file_tags', mode='before')
    @classmethod
    def transform_tags_file(cls, v):
        if not v:
            return []

        if all(hasattr(item, 'tag') for item in v):
            return [item.tag for item in v]

        if all(isinstance(item, dict) and 'tag' in item for item in v):
            return [item['tag'] for item in v]

    class Config:
        from_attributes = True


class TagDTO(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True
