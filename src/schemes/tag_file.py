from uuid import UUID

from pydantic import BaseModel


class AddTagFileDTO(BaseModel):
    id_tag: UUID
    id_file: UUID


class EditTagFileDTO(BaseModel):
    id_tag: UUID | None = None
    id_file: UUID | None = None


class OutputTagFileDTO(BaseModel):
    id: UUID
    id_tag: UUID
    id_file: UUID
