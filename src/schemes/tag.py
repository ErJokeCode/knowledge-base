from uuid import UUID
from pydantic import BaseModel


class AddTagDTO(BaseModel):
    title: str


class EditTagDTO(BaseModel):
    title: str


class OutputTagDTO(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True
