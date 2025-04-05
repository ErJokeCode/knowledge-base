from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from models import Answer, TagAnswer


class QAnswer:
    @staticmethod
    def get_one() -> Select:
        return select(
            Answer
        ).options(
            selectinload(Answer.links),
            selectinload(
                Answer.tag_answers
            ).joinedload(
                TagAnswer.tag
            )
        )
