from uuid import UUID
from pydantic import BaseModel


class AddFileAnswerDTO(BaseModel):
    id_file: UUID
    id_answer: UUID


class EditFileAnswerDTO(BaseModel):
    id_file: UUID | None = None
    id_answer: UUID | None = None


class OutputFileAnswerDTO(BaseModel):
    id: UUID
    id_file: UUID
    id_answer: UUID

    class Config:
        from_attributes = True
