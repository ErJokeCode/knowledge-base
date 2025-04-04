from uuid import UUID
from pydantic import BaseModel


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

    class Config:
        from_attributes = True
