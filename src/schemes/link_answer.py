from uuid import UUID
from pydantic import BaseModel


class AddLinkAnswerDTO(BaseModel):
    id_answer: UUID
    link: str


class EditLinkAnswerDTO(BaseModel):
    id_answer: UUID | None = None
    link: str | None = None


class OutputLinkAnswerDTO(BaseModel):
    id: UUID
    id_answer: UUID
    link: str

    class Config:
        from_attributes = True
