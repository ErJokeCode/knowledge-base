from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import core_pg_orm, ResponseStatus, ListDTO
from depends.database import get_db_session
from schemes.tag import AddTagDTO, EditTagDTO, OutputTagDTO
from schemes.tag_question import AddTagQuestionDTO, OutputTagQuestionDTO


router = APIRouter(
    prefix="/tag",
    tags=["tag"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_tags(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    search: str | None = None,
    sort_by: str | None = None,
    desc: int = 0,
    page: int = 1,
    limit: int = -1,
) -> ListDTO[OutputTagDTO]:
    return await core_pg_orm.tag.get_all(
        session=session,
        search=search,
        search_fields=["title"],
        sort_by=sort_by,
        desc_int=desc,
        page=page,
        limit=limit,
        is_model=False
    )


@router.get("/{id}")
async def get_tag(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> OutputTagDTO:
    return await core_pg_orm.tag.get_by(session=session, id=id, is_model=False)


@router.post("")
async def create_tag(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    data: AddTagDTO
) -> OutputTagDTO:
    return await core_pg_orm.tag.add(
        session=session,
        data=data,
        is_model=False
    )


@router.patch("/{id}")
async def update_tag(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    data: EditTagDTO
) -> OutputTagDTO:
    return await core_pg_orm.tag.edit(
        session=session,
        id=id,
        edit_item=data,
        is_model=False
    )


@router.delete("/{id}")
async def delete_tag(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> ResponseStatus:
    return await core_pg_orm.tag.delete(session=session, id=id)


@router.post("/{id}/question")
async def add_tag_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    id_question: UUID
) -> OutputTagQuestionDTO:
    tag_q = await core_pg_orm.tag_question.get_by(
        session=session,
        id_tag=id,
        id_question=id_question,
        is_model=True,
        is_get_none=True
    )

    if tag_q is not None:
        raise HTTPException(status_code=400, detail="Tag already exists")

    model = AddTagQuestionDTO(id_tag=id, id_question=id_question)
    return await core_pg_orm.tag_question.add(
        session=session,
        data=model
    )


@router.delete("/{id}/question")
async def delete_tag_question(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    id_question: UUID
) -> ResponseStatus:
    model = await core_pg_orm.tag_question.get_by(
        session=session,
        id_tag=id,
        id_question=id_question,
        is_model=True
    )

    return await core_pg_orm.tag_question.delete(
        session=session,
        id=model.id
    )
