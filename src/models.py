

import datetime
import enum
from typing import Annotated

from sqlalchemy import UUID, BigInteger, ForeignKey, Numeric, String, Text
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
bint = Annotated[int, mapped_column(BigInteger)]


# Модель категории
class Category(Base):
    __tablename__ = "category"

    id: Mapped[uuidpk]
    name: Mapped[str_64]
    description: Mapped[str_255]

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
    rating: Mapped[num_] = mapped_column(default=0.0)

    created_at: Mapped[datetime_] = mapped_column(
        default=datetime.datetime.now
    )

    question: Mapped["Question"] = relationship(
        back_populates="answers"
    )
    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="answer"
    )
    tag_answers: Mapped[list["TagAnswer"]] = relationship(
        back_populates="answer"
    )
    links: Mapped[list["LinkAnswer"]] = relationship(
        back_populates="answer"
    )
    files: Mapped[list["MinioFileAnswer"]] = relationship(
        back_populates="answer"
    )


class LinkAnswer(Base):
    __tablename__ = "link"

    id: Mapped[uuidpk]
    id_answer: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE")
    )
    link: Mapped[text]

    answer: Mapped["Answer"] = relationship(
        back_populates="links"
    )


class TypeTag(enum.Enum):
    question = "question"
    answer = "answer"
    file = "file"


# Модель тега для вопроса
class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[uuidpk]

    title: Mapped[str_64]
    type: Mapped[TypeTag]

    tag_questions: Mapped[list["TagQuestion"]] = relationship(
        back_populates="tag"
    )
    tag_answers: Mapped[list["TagAnswer"]] = relationship(
        back_populates="tag"
    )
    tag_files: Mapped[list["TagFile"]] = relationship(
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


class TagAnswer(Base):
    __tablename__ = "tag_answer"

    id: Mapped[uuidpk]
    id_answer: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE")
    )
    id_tag: Mapped[UUID] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE")
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="tag_answers"
    )
    answer: Mapped["Answer"] = relationship(
        back_populates="tag_answers"
    )


class TagFile(Base):
    __tablename__ = "tag_file"

    id: Mapped[uuidpk]
    id_tag: Mapped[UUID] = mapped_column(
        ForeignKey("tag.id")
    )
    id_file: Mapped[UUID] = mapped_column(
        ForeignKey("minio_file.id")
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="tag_files"
    )
    file: Mapped["MinioFile"] = relationship(
        back_populates="tag_files"
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


# Модель файла в minio
class MinioFile(Base):
    __tablename__ = "minio_file"

    id: Mapped[uuidpk]
    id_tag: Mapped[UUID] = mapped_column(
        ForeignKey("tag.id")
    )

    filename: Mapped[str_64]
    bucket_name: Mapped[str_64]
    key: Mapped[str_128]
    size: Mapped[bint]
    created_at: Mapped[datetime_] = mapped_column(
        default=datetime.datetime.now
    )

    tag_files: Mapped[list["TagFile"]] = relationship(
        back_populates="file"
    )
    answers: Mapped[list["MinioFileAnswer"]] = relationship(
        back_populates="file"
    )


class MinioFileAnswer(Base):
    __tablename__ = "minio_file_answer"

    id: Mapped[uuidpk]
    id_file: Mapped[UUID] = mapped_column(
        ForeignKey("minio_file.id", ondelete="CASCADE")
    )
    id_answer: Mapped[UUID] = mapped_column(
        ForeignKey("answer.id", ondelete="CASCADE")
    )

    answer: Mapped["Answer"] = relationship(
        back_populates="files"
    )
    file: Mapped["MinioFile"] = relationship(
        back_populates="answers"
    )
