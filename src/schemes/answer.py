import datetime
from uuid import UUID
from pydantic import BaseModel, field_validator


class InputAnswerDTO(BaseModel):
    id_question: UUID
    answer: str
    links: list[str] | None = None
    tag_ids: list[UUID] | None = None


class AddAnswerDTO(BaseModel):
    id_question: UUID
    answer: str


class EditAnswerDTO(BaseModel):
    id_question: UUID | None = None
    answer: str | None = None


class OutputAnswerDTO(BaseModel):
    id: UUID
    id_question: UUID
    answer: str
    rating: float
    created_at: datetime.datetime

    links: list["LinkDTO"] | None
    tag_answers: list["TagAnswerDTO"]

    @field_validator('tag_answers', mode='before')
    @classmethod
    def transform_tags(cls, v):
        if not v:
            return []

        # Если пришли объекты TagQuestion
        if all(hasattr(item, 'tag') for item in v):
            return [item.tag for item in v]

        # Если пришли словари с вложенностью
        if all(isinstance(item, dict) and 'tag' in item for item in v):
            return [item['tag'] for item in v]

        return v

    class Config:
        from_attributes = True


class TagAnswerDTO(BaseModel):
    tag: "TagDTO"

    class Config:
        from_attributes = True


class TagDTO(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True


class LinkDTO(BaseModel):
    id: UUID
    link: str

    class Config:
        from_attributes = True
