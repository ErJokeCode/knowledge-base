from uuid import UUID
from pydantic import BaseModel


class AddTagAnswerDTO(BaseModel):
    id_answer: UUID
    id_tag: UUID


class EditTagAnswerDTO(BaseModel):
    id_answer: UUID | None = None
    id_tag: UUID | None = None


class OutputTagAnswerDTO(BaseModel):
    id: UUID
    id_answer: UUID
    id_tag: UUID

    class Config:
        from_attributes = True
