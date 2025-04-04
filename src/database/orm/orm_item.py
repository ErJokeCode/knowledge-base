import logging
from typing import Literal, Sequence, TypeVar, Generic, overload
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, Select, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm.list_pagination import ListDTO
from database.postgres_core import Base


_log = logging.getLogger(__name__)


M = TypeVar('M')
I = TypeVar('I', bound=BaseModel)
E = TypeVar('E', bound=BaseModel)
O = TypeVar('O', bound=BaseModel)


class ItemOrm(Generic[M, I, E, O]):
    def __init__(self, model: type[M], input_scheme: type[I], edit_schema: type[E], out_scheme: type[O]) -> None:
        self.model = model
        self.input_scheme = input_scheme
        self.edit_schema = edit_schema
        self.out_scheme = out_scheme

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[True] = True
    ) -> M: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        *,
        is_model: Literal[False]
    ) -> O: ...

    @overload
    async def add(
        self,
        session: AsyncSession,
        data: I,
        is_return: Literal[False]
    ) -> None: ...

    async def add(self, session: AsyncSession, data: I, is_return: bool = True, is_model: bool = True) -> M | O | None:
        _log.info("Add %s. Return model", self.model.__name__)

        model = self.model(**data.model_dump())
        session.add(model)
        await session.flush()

        if not is_return:
            return None

        if is_model:
            return model

        return self.out_scheme.model_validate(model)

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        *,
        has_is_active: bool = False,
        is_pagination: Literal[True],
        is_model: Literal[True]
    ) -> ListDTO[M]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[False],
        is_model: Literal[True]
    ) -> Sequence[M]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[True],
        is_model: Literal[False]
    ) -> ListDTO[O]: ...

    @overload
    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        *,
        is_pagination: Literal[False],
        is_model: Literal[False]
    ) -> Sequence[O]: ...

    async def get_all(
        self,
        session: AsyncSession,
        query_select: Select | None = None,
        sort_by: str | None = None,
        desc_int: int = 0,
        page: int = 1,
        limit: int = -1,
        has_is_active: bool = False,
        is_pagination: bool = True,
        is_model: bool = True
    ) -> ListDTO[O] | Sequence[O] | ListDTO[M] | Sequence[M]:
        _log.info("Get all %s", self.model.__name__)

        if query_select is None:
            query_select = select(self.model)

        if page < 1:
            raise HTTPException(
                status_code=400, detail="Page number must be greater than 0"
            )

        if has_is_active:
            query_select = query_select.filter(
                self.model.is_active == True)  # type: ignore

        if is_pagination:
            q_total_record = query_select

        if sort_by:
            query_select = query_select.order_by(
                desc(getattr(self.model, sort_by)) if desc_int else asc(
                    getattr(self.model, sort_by))
            )

        query_select = query_select.offset((page - 1) * limit)
        if limit != -1:
            query_select = query_select.limit(limit)

        result = await session.execute(query_select)
        content = result.scalars().all()

        if is_pagination:
            q_total_record = q_total_record.with_only_columns(
                func.count(self.model.id))  # type: ignore
            r_total_record = await session.execute(q_total_record)
            total_record = r_total_record.scalar_one_or_none()

            if total_record is None:
                total_record = 0

            if limit == -1:
                pages = 1
            else:
                pages = total_record // limit if total_record % limit == 0 else total_record // limit + 1

            if is_model:
                return ListDTO[M](
                    page_number=page,
                    page_size=limit if limit != -1 else total_record,
                    total_pages=pages,
                    total_record=total_record,
                    content=[item for item in content]
                )
            else:
                return ListDTO[O](
                    page_number=page,
                    page_size=limit if limit != -1 else total_record,
                    total_pages=pages,
                    total_record=total_record,
                    content=[self.out_scheme.model_validate(
                        item) for item in content]
                )
        else:
            if is_model:
                return content
            else:
                return [self.out_scheme.model_validate(item) for item in content]

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        *,
        is_model: Literal[True],
        is_get_none: Literal[False],
        **kwargs
    ) -> M: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        *,
        is_model: Literal[False],
        is_get_none: Literal[False],
        **kwargs
    ) -> O: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        *,
        is_model: Literal[True],
        is_get_none: Literal[True],
        **kwargs
    ) -> M | None: ...

    @overload
    async def get_by(
        self,
        session: AsyncSession,
        *,
        is_model: Literal[False],
        is_get_none: Literal[True],
        **kwargs
    ) -> O | None: ...

    async def get_by(
            self,
            session: AsyncSession,
            is_model: bool = True,
            is_get_none: bool = True,
            **kwargs) -> O | M | None:
        _log.info("Get by kwargs %s", self.model.__name__)

        query = select(
            self.model
        ).filter_by(
            **kwargs
        )

        result = await session.execute(query)
        item = result.scalars().first()

        if item is None:
            if is_get_none:
                return None
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if is_model:
            return item

        return self.out_scheme.model_validate(item)

    async def get_model_by_query(self, session: AsyncSession, query: Select, get_none: bool = False) -> M:
        _log.info("Get model by query %s", self.model.__name__)

        result = await session.execute(query)
        item = result.scalars().first()

        if item is None and not get_none:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        return item  # type: ignore

    async def edit(self, session: AsyncSession, id: UUID, edit_item: E | dict, return_query: Select | None = None) -> O:
        _log.info("Edit %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if isinstance(edit_item, dict):
            for key, value in edit_item.items():
                if value is not None:
                    setattr(model, key, value)
        else:
            for key, value in edit_item.model_dump().items():
                if value is not None:
                    setattr(model, key, value)

        await session.flush()

        if return_query is not None:
            return await self.get_by_query(session, return_query)

        return self.out_scheme.model_validate(model)

    async def edit_model(self, session: AsyncSession, id: UUID, edit_item: E | dict) -> M:
        _log.info("Edit model %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        if isinstance(edit_item, dict):
            for key, value in edit_item.items():
                if value is not None:
                    setattr(model, key, value)
        else:
            for key, value in edit_item.model_dump().items():
                if value is not None:
                    setattr(model, key, value)

        await session.flush()
        return model

    async def get_by_id(self, session: AsyncSession, id: UUID, get_none: bool = False) -> O:
        _log.info("Get by id %s", self.model.__name__)

        model = await session.get(self.model, id)

        if model is None and get_none is False:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")
        if model is None and get_none is True:
            return None  # type: ignore

        return self.out_scheme.model_validate(model)

    async def get_by_query(self, session: AsyncSession, query: Select) -> O:
        _log.info("Get by query %s", self.model.__name__)

        result = await session.execute(query)
        model = result.scalars().first()

        if model is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        return self.out_scheme.model_validate(model)

    async def get_model_by(self, session: AsyncSession, **kwargs) -> M | None:
        _log.info("Get model by kwargs %s", self.model.__name__)

        model = select(self.model).filter_by(**kwargs)
        result = await session.execute(model)
        return result.scalars().first()

    async def get_model_by_id(self, session: AsyncSession, id: UUID, get_none: bool = False) -> M:
        _log.info("Get model by id %s", self.model.__name__)

        res = await self.get_model_by(session, id=id)

        if res is None and not get_none:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found")

        return res  # type: ignore

    async def in_db(self, session: AsyncSession, item_ids: list[UUID]) -> bool:
        _log.info("In db %s", self.model.__name__)

        for institute_id in item_ids:
            query = select(self.model).filter(
                self.model.id == institute_id)  # type: ignore
            result = await session.execute(query)
            institute = result.scalars().first()
            if institute is None:
                return False
        return True

    async def delete(self, session: AsyncSession, id: UUID, query_has_child: Select | None = None) -> None:
        _log.info("Delete %s", self.model.__name__)

        model = None
        if query_has_child is not None:
            res = await session.execute(query_has_child)
            model = res.scalars().first()

        if model is not None:
            await self.edit_model(session, id, {"is_active": False})
        else:
            del_model = await session.get(self.model, id)

            if del_model is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.model.__name__} not found")

            await session.delete(del_model)

    async def query(self, session: AsyncSession, query: Select) -> Result:
        _log.info("Query %s", self.model.__name__)

        result = await session.execute(query)
        return result


class BaseItemOrm:
    def __init__(self) -> None:
        pass

    async def get_all_query(self, session: AsyncSession, query: Select) -> Sequence:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.scalars().all()

        return items

    async def get_dict_query(self, session: AsyncSession, query: Select) -> dict:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.tuples().all()

        return {item[0]: item[1] for item in items}

    async def get_tuple_query(self, session: AsyncSession, query: Select) -> Sequence:
        _log.info("Base query")

        result = await session.execute(query)
        items = result.tuples().all()

        return items
