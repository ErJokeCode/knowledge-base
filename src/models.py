

import datetime
from typing import Annotated

from sqlalchemy import UUID, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from database.base import Base


uuidpk = Annotated[UUID, mapped_column(
    UUID(), default=uuid.uuid4, primary_key=True)]
str_64 = Annotated[str, mapped_column(String(64))]
str_128 = Annotated[str, mapped_column(String(128))]
str_255 = Annotated[str, mapped_column(String(255))]
str_500 = Annotated[str, mapped_column(String(500))]
text = Annotated[str, mapped_column(Text)]
datetime_ = Annotated[datetime.datetime, mapped_column()]
num_ = Annotated[Numeric, mapped_column(Numeric(precision=4, scale=3))]


# Модель категории
class Category(Base):
    __tablename__ = "category"

    id: Mapped[uuidpk]
    name: Mapped[str_64]
    description: Mapped[str_255]
    is_active: Mapped[bool] = mapped_column(default=True)

    questions: Mapped[list["Question"]] = relationship(
        back_populates="category"
    )


# Модель вопроса
class Question(Base):
    __tablename__ = "question"

    id: Mapped[uuidpk]
    id_category: Mapped[UUID] = mapped_column(
        ForeignKey("category.id", ondelete="CASCADE")
    )

    question: Mapped[text]

    created_at: Mapped[datetime_] = mapped_column(
        default=datetime.datetime.now
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    category: Mapped["Category"] = relationship(
        back_populates="questions"
    )
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question"
    )
    tag_questions: Mapped[list["TagQuestion"]] = relationship(
        back_populates="question"
    )


# Модель ответа
class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[uuidpk]
    id_question: Mapped[UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )

    answer: Mapped[text]
    link: Mapped[text]

    created_at: Mapped[datetime_] = mapped_column(
        default=datetime.datetime.now
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    question: Mapped["Question"] = relationship(
        back_populates="answers"
    )
    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="answer"
    )


# Модель тега для вопроса
class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[uuidpk]

    title: Mapped[str_64]

    tag_questions: Mapped[list["TagQuestion"]] = relationship(
        back_populates="tag"
    )


class TagQuestion(Base):
    __tablename__ = "tag_question"

    id: Mapped[uuidpk]
    id_question: Mapped[UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )
    id_tag: Mapped[UUID] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE")
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="tag_questions"
    )
    question: Mapped["Question"] = relationship(
        back_populates="tag_questions"
    )


# Модель оценки ответа
class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[uuidpk]
    id_ansawer: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE")
    )

    mark: Mapped[int]
    created_at: Mapped[datetime_] = mapped_column(
        default=datetime.datetime.now
    )

    answer: Mapped["Answer"] = relationship(
        back_populates="feedbacks"
    )

# # Модель файла в minio
# class MinioFile(Base):
#     __tablename__ = "minio_file"
