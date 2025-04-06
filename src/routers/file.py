import logging
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse

from database import core_pg_orm, core_s3
from depends.database import get_db_session

_log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/file",
    tags=["file"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}/download")
async def get_file(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
) -> StreamingResponse:
    info_file = await core_pg_orm.file.get_by(session=session, id=id, is_model=False)
    _log.info(info_file)
    return StreamingResponse(
        content=core_s3.download_file(file_key=str(info_file.id)),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={info_file.filename}"}
    )


@router.delete("/{id}")
async def delete_file(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    id: UUID
):
    resp = await core_pg_orm.file.delete(session=session, id=id)

    await core_s3.delete_file(file_key=str(id))

    return resp
