from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from models import Answer, MinioFile, MinioFileAnswer, Question, TagAnswer, TagFile, TagQuestion


class QQuestion:
    @staticmethod
    def get_one() -> Select:
        return select(
            Question
        ).options(
            selectinload(
                Question.answers
            ).selectinload(
                Answer.answer_tags
            ).joinedload(
                TagAnswer.tag
            ),

            selectinload(
                Question.answers
            ).selectinload(
                Answer.links
            ),

            selectinload(
                Question.answers
            ).selectinload(
                Answer.files
            ).joinedload(
                MinioFileAnswer.file
            ).selectinload(
                MinioFile.file_tags
            ).joinedload(
                TagFile.tag
            ),

            selectinload(
                Question.question_tags
            ).joinedload(
                TagQuestion.tag
            )
        )

    @staticmethod
    def get_all(
            search: str | None = None,
            id_category: UUID | None = None,
            id_tag: UUID | None = None,
    ) -> Select:
        query = select(
            Question
        )

        if search:
            query = query.filter(
                Question.question.like(f"%{search}%")
            )

        if id_category:
            query = query.filter(
                Question.id_category == id_category
            )

        if id_tag:
            query = query.filter(
                Question.question_tags.any(
                    TagQuestion.id_tag == id_tag
                )
            )

        query = query.options(
            selectinload(
                Question.answers
            ).selectinload(
                Answer.answer_tags
            ).joinedload(
                TagAnswer.tag
            ),

            selectinload(
                Question.answers
            ).selectinload(
                Answer.links
            ),

            selectinload(
                Question.answers
            ).selectinload(
                Answer.files
            ).joinedload(
                MinioFileAnswer.file
            ).selectinload(
                MinioFile.file_tags
            ).joinedload(
                TagFile.tag
            ),

            selectinload(
                Question.question_tags
            ).joinedload(
                TagQuestion.tag
            )
        )

        return query
