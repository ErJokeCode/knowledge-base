import datetime
from uuid import UUID
from pydantic import BaseModel


class InputQuestionDTO(BaseModel):
    id_category: UUID
    question: str


class AddQuestionDTO(BaseModel):
    id_category: UUID
    question: str


class EditQuestionDTO(BaseModel):
    id_category: UUID | None = None
    question: str | None = None


class OutputQuestionDTO(BaseModel):
    id: UUID
    id_category: UUID
    question: str
    created_at: datetime.datetime
    is_active: bool

    class Config:
        from_attributes = True
