from database.orm.orm_item import BaseItemOrm, ItemOrm

from models import Category, Question, Answer, Tag, TagQuestion
from schemes.category import AddCategoryDTO, EditCategoryDTO, OutputCategoryDTO
from schemes.question import AddQuestionDTO, EditQuestionDTO, OutputQuestionDTO
from schemes.answer import AddAnswerDTO, EditAnswerDTO, OutputAnswerDTO
from schemes.tag import AddTagDTO, EditTagDTO, OutputTagDTO
from schemes.tag_question import AddTagQuestionDTO, EditTagQuestionDTO, OutputTagQuestionDTO


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

        self.tag = ItemOrm(
            Tag, AddTagDTO,
            EditTagDTO, OutputTagDTO
        )

        self.tag_question = ItemOrm(
            TagQuestion, AddTagQuestionDTO,
            EditTagQuestionDTO, OutputTagQuestionDTO
        )
