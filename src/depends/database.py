import logging
from typing import AsyncGenerator
from uuid import UUID
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from database import core_postgres

_log = logging.getLogger(__name__)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with core_postgres.session_factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            _log.error(error)
            raise HTTPException(status_code=500, detail="Database error")

        finally:
            await session.close()
