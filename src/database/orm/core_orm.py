from database.orm.orm_item import BaseItemOrm, ItemOrm

from models import Category, Question, Answer
from schemes.category import AddCategoryDTO, EditCategoryDTO, OutputCategoryDTO
from schemes.question import AddQuestionDTO, EditQuestionDTO, OutputQuestionDTO
from schemes.answer import AddAnswerDTO, EditAnswerDTO, OutputAnswerDTO


class CoreOrm:
    def __init__(self) -> None:
        self.base = BaseItemOrm()

        self.category = ItemOrm(
            Category, AddCategoryDTO,
            EditCategoryDTO, OutputCategoryDTO
        )

        self.question = ItemOrm(
            Question, AddQuestionDTO,
            EditQuestionDTO, OutputQuestionDTO
        )

        self.answer = ItemOrm(
            Answer, AddAnswerDTO,
            EditAnswerDTO, OutputAnswerDTO
        )
