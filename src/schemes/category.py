from uuid import UUID
from pydantic import BaseModel

from schemes.question import OutputQuestionDTO


class InputCategoryDTO(BaseModel):
    name: str
    description: str


class AddCategoryDTO(BaseModel):
    name: str
    description: str


class EditCategoryDTO(BaseModel):
    name: str | None = None
    description: str | None = None


class OutputCategoryDTO(BaseModel):
    id: UUID
    name: str
    description: str
    questions: list[OutputQuestionDTO] = []

    class Config:
        from_attributes = True
