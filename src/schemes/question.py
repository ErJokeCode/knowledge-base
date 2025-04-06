import datetime
from uuid import UUID
from pydantic import BaseModel, field_validator

from schemes.answer import OutputAnswerDTO


class InputQuestionDTO(BaseModel):
    id_category: UUID
    question: str


class AddQuestionDTO(BaseModel):
    id_category: UUID
    question: str


class EditQuestionDTO(BaseModel):
    id_category: UUID | None = None
    question: str | None = None


class OutputQuestionDTO(BaseModel):
    id: UUID
    id_category: UUID
    question: str
    created_at: datetime.datetime

    answers: list[OutputAnswerDTO] = []
    question_tags: list["Tag"] = []

    @field_validator('question_tags', mode='before')
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


class TagQuestion(BaseModel):
    tag: "Tag"

    class Config:
        from_attributes = True


class Tag(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True
