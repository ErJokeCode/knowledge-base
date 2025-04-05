from uuid import UUID

from pydantic import BaseModel


class InputTagQuestionDTO(BaseModel):
    id_tag: UUID
    id_question: UUID


class AddTagQuestionDTO(BaseModel):
    id_tag: UUID
    id_question: UUID


class EditTagQuestionDTO(BaseModel):
    id_tag: UUID | None = None
    id_question: UUID | None = None


class OutputTagQuestionDTO(BaseModel):
    id: UUID
    id_tag: UUID
    id_question: UUID

    class Config:
        from_attributes = True
