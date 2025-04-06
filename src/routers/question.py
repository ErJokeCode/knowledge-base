from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm.base_schemes import ListDTO
from depends.database import get_db_session
from schemes.question import EditQuestionDTO, InputQuestionDTO, OutputQuestionDTO
from database import core_pg_orm, ResponseStatus
from services.question.query import QQuestion


router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_questions(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    search: str | None = None,
    id_category: UUID | None = None,
    id_tag: UUID | None = None,
    sort_by: str | None = None,
    desc: int = 0,
    page: int = 1,
    limit: int = -1
) -> ListDTO[OutputQuestionDTO]:
    return await core_pg_orm.question.get_all(
        session=session,
        query_select=QQuestion.get_all(
            search=search,
            id_category=id_category,
            id_tag=id_tag
        ),
        sort_by=sort_by,
        desc_int=desc,
        page=page,
        limit=limit,
        is_pagination=True,
        is_model=False
    )


@router.get("/{id}")
async def get_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> OutputQuestionDTO:
    return await core_pg_orm.question.get_by_query(
        session=session,
        query=QQuestion.get_one(),
        id=id,
        is_model=False
    )


@router.post("")
async def create_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    data: InputQuestionDTO
) -> OutputQuestionDTO:
    return await core_pg_orm.question.add(
        session=session,
        data=data,
        is_model=False,
        return_query=QQuestion.get_one()
    )


@router.patch("/{id}")
async def update_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    data: EditQuestionDTO
) -> OutputQuestionDTO:
    return await core_pg_orm.question.edit(
        session=session,
        id=id,
        edit_item=data,
        is_model=False,
        return_query=QQuestion.get_one()
    )


@router.delete("/{id}")
async def delete_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> ResponseStatus:
    return await core_pg_orm.question.delete(session=session, id=id)
