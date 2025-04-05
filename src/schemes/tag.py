from uuid import UUID
from pydantic import BaseModel

from models import TypeTag


class AddTagDTO(BaseModel):
    title: str
    type: TypeTag


class EditTagDTO(BaseModel):
    title: str | None = None
    type: TypeTag | None = None


class OutputTagDTO(BaseModel):
    id: UUID
    title: str
    type: TypeTag

    class Config:
        from_attributes = True
