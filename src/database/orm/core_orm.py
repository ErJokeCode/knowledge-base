from database.orm.orm_item import BaseItemOrm, ItemOrm

from models import Category, LinkAnswer, Question, Answer, Tag, TagAnswer, TagQuestion
from schemes.category import AddCategoryDTO, EditCategoryDTO, OutputCategoryDTO
from schemes.link_answer import AddLinkAnswerDTO, EditLinkAnswerDTO, OutputLinkAnswerDTO
from schemes.question import AddQuestionDTO, EditQuestionDTO, OutputQuestionDTO
from schemes.answer import AddAnswerDTO, EditAnswerDTO, OutputAnswerDTO
from schemes.tag import AddTagDTO, EditTagDTO, OutputTagDTO
from schemes.tag_answer import AddTagAnswerDTO, EditTagAnswerDTO, OutputTagAnswerDTO
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

        self.link = ItemOrm(
            LinkAnswer, AddLinkAnswerDTO,
            EditLinkAnswerDTO, OutputLinkAnswerDTO
        )

        self.tag_answer = ItemOrm(
            TagAnswer, AddTagAnswerDTO,
            EditTagAnswerDTO, OutputTagAnswerDTO
        )
