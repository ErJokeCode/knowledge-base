from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from models import Answer, Question, TagQuestion


class QQuestion:
    @staticmethod
    def get_one() -> Select:
        return select(
            Question
        ).options(
            selectinload(
                Question.answers
            ).selectinload(
                Answer.tag_answers
            ),
            selectinload(
                Question.answers
            ).selectinload(
                Answer.links
            ),
            selectinload(
                Question.tag_questions
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
                Question.tag_questions.any(
                    TagQuestion.id_tag == id_tag
                )
            )

        query = query.options(
            selectinload(
                Question.answers
            ).selectinload(
                Answer.tag_answers
            ),
            selectinload(
                Question.answers
            ).selectinload(
                Answer.links
            ),
            selectinload(
                Question.tag_questions
            ).joinedload(
                TagQuestion.tag
            )
        )

        return query
