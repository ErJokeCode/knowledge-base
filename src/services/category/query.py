from uuid import UUID
from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from models import Category, Question, TagQuestion


class QCategory:
    @staticmethod
    def get_one() -> Select:
        return select(
            Category
        ).options(
            selectinload(
                Category.questions
            ).selectinload(
                Question.answers
            ),
            selectinload(
                Category.questions
            ).selectinload(
                Question.tag_questions
            ).selectinload(
                TagQuestion.tag
            )
        )

    @staticmethod
    def get_all(
        search: str | None = None,
        id_tag: UUID | None = None
    ) -> Select:
        query = select(
            Category
        )

        if search:
            query = query.filter(
                Category.name.like(f"%{search}%")
            )

        if id_tag:
            query = query.filter(
                Category.questions.any(
                    Question.tag_questions.any(
                        TagQuestion.id_tag == id_tag
                    )
                )
            )

        query = query.options(
            selectinload(
                Category.questions
            ).selectinload(
                Question.answers
            ),
            selectinload(
                Category.questions
            ).selectinload(
                Question.tag_questions
            ).selectinload(
                TagQuestion.tag
            )
        )

        return query
