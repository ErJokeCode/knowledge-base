from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm.list_pagination import ListDTO
from depends.database import get_db_session

from database import core_pg_orm
from schemes.category import AddCategoryDTO, OutputCategoryDTO


router = APIRouter(
    prefix="/category",
    tags=["category"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_categories(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    sort_by: str | None = None,
    desc: int = 0,
    page: int = 1,
    limit: int = -1
) -> ListDTO[OutputCategoryDTO]:
    return await core_pg_orm.category.get_all(
        session=session, sort_by=sort_by, desc_int=desc, page=page,
        limit=limit, has_is_active=True, is_pagination=True, is_model=False
    )


@router.get("/{id}")
async def get_category(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: str
):
    return await core_pg_orm.category.get_by(
        session=session, is_model=False, is_get_none=False, id=id
    )


@router.post("/")
async def create_category(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    data: AddCategoryDTO
) -> OutputCategoryDTO:
    return await core_pg_orm.category.add(
        session=session, data=data, is_model=False
    )


@router.put("/{id}")
async def update_category(id: str):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{id}")
async def delete_category(id: str):
    raise HTTPException(status_code=501, detail="Not implemented")
