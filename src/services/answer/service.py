import logging
from uuid import UUID
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import core_pg_orm, core_s3
from database.orm.base_schemes import ResponseStatus
from schemes.answer import AddAnswerDTO, InputAnswerDTO, OutputAnswerDTO
from schemes.file import AddFileDTO
from schemes.file_answer import AddFileAnswerDTO
from schemes.link_answer import AddLinkAnswerDTO
from schemes.tag_answer import AddTagAnswerDTO
from services.answer.query import QAnswer
from config import settings

_log = logging.getLogger(__name__)


class SAnswer:
    def __init__(self) -> None:
        pass

    async def add_answer(
        self,
        session: AsyncSession,
        data: InputAnswerDTO
    ):
        a_answer = AddAnswerDTO(
            id_question=data.id_question,
            answer=data.answer
        )

        m_answer = await core_pg_orm.answer.add(
            session=session,
            data=a_answer
        )

        if data.links is not None:
            for link in data.links:
                m_link = AddLinkAnswerDTO(
                    id_answer=m_answer.id,
                    link=link
                )
                await core_pg_orm.link.add(
                    session=session,
                    data=m_link
                )
        if data.tag_ids is not None:
            for tag in data.tag_ids:
                m_tag = await core_pg_orm.tag.get_by(
                    session=session,
                    id=tag,
                    is_model=True
                )

                a_tag_answer = AddTagAnswerDTO(
                    id_answer=m_answer.id,
                    id_tag=m_tag.id
                )

                await core_pg_orm.tag_answer.add(
                    session=session,
                    data=a_tag_answer
                )

        return await core_pg_orm.answer.get_by_query(
            session=session,
            query=QAnswer.get_one(),
            id=UUID(str(m_answer.id)),
            is_model=False,
            is_get_none=False
        )

    async def add_tag_answer(
        self,
        session: AsyncSession,
        id: UUID,
        id_tag: UUID
    ) -> OutputAnswerDTO:
        get_tag = await core_pg_orm.tag_answer.get_by(
            session=session,
            id_tag=id_tag,
            id_answer=id,
            is_model=True,
            is_get_none=True
        )

        if get_tag is not None:
            raise HTTPException(status_code=400, detail="Tag already exists")

        a_model = AddTagAnswerDTO(
            id_answer=id,
            id_tag=id_tag
        )

        await core_pg_orm.tag_answer.add(
            session=session,
            data=a_model,
            is_model=False,
        )

        return await core_pg_orm.answer.get_by_query(
            session=session,
            query=QAnswer.get_one(),
            id=id,
            is_model=False
        )

    async def delete_tag_answer(
        self,
        session: AsyncSession,
        id: UUID,
        id_tag: UUID
    ) -> ResponseStatus:
        m_tag = await core_pg_orm.tag_answer.get_by(
            session=session,
            id_tag=id_tag,
            id_answer=id,
            is_model=True
        )

        return await core_pg_orm.tag_answer.delete(
            session=session,
            id=m_tag.id
        )

    async def add_link_answer(
        self,
        session: AsyncSession,
        id: UUID,
        link: str
    ) -> OutputAnswerDTO:
        await core_pg_orm.link.add(
            session=session,
            data=AddLinkAnswerDTO(
                id_answer=id,
                link=link
            )
        )

        return await core_pg_orm.answer.get_by_query(
            session=session,
            query=QAnswer.get_one(),
            id=id,
            is_model=False
        )

    async def delete_link_answer(
        self,
        session: AsyncSession,
        id: UUID
    ) -> ResponseStatus:
        return await core_pg_orm.link.delete(
            session=session,
            id=id
        )

    async def add_file_answer(
        self,
        session: AsyncSession,
        id: UUID,
        files: list[UploadFile] | UploadFile | None
    ) -> OutputAnswerDTO:
        if files is None:
            return await core_pg_orm.answer.get_by_query(
                session=session,
                query=QAnswer.get_one(),
                id=id,
                is_model=False
            )

        if isinstance(files, list):
            for file in files:
                await self.__add_file(session=session, id=id, file=file)
        else:
            file = files
            await self.__add_file(session=session, id=id, file=file)

        return await core_pg_orm.answer.get_by_query(
            session=session,
            query=QAnswer.get_one(),
            id=id,
            is_model=False
        )

    async def __add_file(
        self,
        session: AsyncSession,
        id: UUID,
        file: UploadFile
    ) -> None:
        a_file = AddFileDTO(
            filename=file.filename,
            bucket_name=settings.MINIO_BUCKET_NAME,
            size=file.size // 1024 if file.size is not None else None,
        )

        m_file = await core_pg_orm.file.add(
            session=session,
            data=a_file,
            is_model=False
        )

        await core_s3.upload_file(
            file_key=str(m_file.id),
            file=file
        )

        a_file_answer = AddFileAnswerDTO(
            id_file=m_file.id,
            id_answer=id,
        )

        await core_pg_orm.file_answer.add(
            session=session,
            data=a_file_answer
        )

    async def delete_file_answer(
        self,
        session: AsyncSession,
        id: UUID,
        id_file: UUID
    ) -> ResponseStatus:
        file_ans = await core_pg_orm.file_answer.get_by(
            session=session,
            id_answer=id,
            id_file=id_file,
            is_model=False
        )

        resp = await core_pg_orm.file_answer.delete(
            session=session,
            id=file_ans.id
        )

        file_ans_try = await core_pg_orm.file_answer.get_by(
            session=session,
            id_file=id_file
        )

        if file_ans_try is None:
            await core_pg_orm.file.delete(
                session=session,
                id=id_file
            )

            await core_s3.delete_file(
                file_key=str(id_file)
            )

        return resp
