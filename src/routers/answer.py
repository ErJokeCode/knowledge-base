from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import core_pg_orm, ResponseStatus
from schemes.tag_answer import AddTagAnswerDTO
from services import s_answer
from depends.database import get_db_session
from schemes.answer import AddAnswerDTO, EditAnswerDTO, InputAnswerDTO, OutputAnswerDTO
from services.answer.query import QAnswer


router = APIRouter(
    prefix="/answer",
    tags=["answer"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def create_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    data: InputAnswerDTO
) -> OutputAnswerDTO:
    return await s_answer.add_answer(
        session=session,
        data=data,
    )


@router.patch("/{id}")
async def update_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    data: EditAnswerDTO
) -> OutputAnswerDTO:
    return await core_pg_orm.answer.edit(
        session=session,
        id=id,
        edit_item=data,
        is_model=False,
        return_query=QAnswer.get_one()
    )


@router.delete("/{id}")
async def delete_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
) -> ResponseStatus:
    return await core_pg_orm.answer.delete(
        session=session,
        id=id
    )


@router.post("/{id}/link")
async def add_link_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    link: str
) -> OutputAnswerDTO:
    return await s_answer.add_link_answer(
        session=session,
        id=id,
        link=link
    )


@router.delete("/{id}/link")
async def delete_link_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> ResponseStatus:
    return await s_answer.delete_link_answer(
        session=session,
        id=id
    )


@router.post("/{id}/file")
async def add_file_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    files: list[UploadFile] | UploadFile | None
) -> OutputAnswerDTO:
    return await s_answer.add_file_answer(
        session=session,
        id=id,
        files=files
    )


@router.delete("/{id}/file/{file_id}")
async def delete_file_answer(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID,
    id_file: UUID
) -> OutputAnswerDTO:
    return await s_answer.delete_file_answer(
        session=session,
        id=id,
        id_file=id_file
    )
