import datetime
from uuid import UUID
from pydantic import BaseModel


class InputAnswerDTO(BaseModel):
    id_question: UUID
    answer: str
    link: str | None


class AddAnswerDTO(BaseModel):
    id_question: UUID
    answer: str
    link: str


class EditAnswerDTO(BaseModel):
    id_question: UUID | None = None
    answer: str | None = None
    link: str | None


class OutputAnswerDTO(BaseModel):
    id: UUID
    id_question: UUID
    answer: str
    link: str
    created_at: datetime.datetime
    is_active: bool

    class Config:
        from_attributes = True
