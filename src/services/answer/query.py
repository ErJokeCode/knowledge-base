from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload

from models import Answer, MinioFile, MinioFileAnswer, TagAnswer, TagFile


class QAnswer:
    @staticmethod
    def get_one() -> Select:
        return select(
            Answer
        ).options(
            selectinload(Answer.links),
            selectinload(
                Answer.answer_tags
            ).joinedload(
                TagAnswer.tag
            ),
            selectinload(
                Answer.files
            ).joinedload(
                MinioFileAnswer.file
            ).selectinload(
                MinioFile.file_tags
            ).joinedload(
                TagFile.tag
            )
        )
