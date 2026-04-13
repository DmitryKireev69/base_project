from pydantic import BaseModel
from sqlalchemy import select, delete, update
from typing import Any, Dict



class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filer):
        query = select(self.model).filter_by(**filer)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        obj = self.model(**data.model_dump())
        self.session.add(obj)
        return obj

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> dict[str, str]:
        stmp = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model.id)
        )
        result = await self.session.execute(stmp)
        objects = result.scalars().all()
        if not objects:
            return {'message': 'Не удалось найти обьект по указанным полям!'}

        return {'message': 'Обновление успешно!'}


    async def delete(self, **filter_by) -> dict[str, str]:
        stmp = delete(self.model).filter_by(**filter_by).returning(self.model.id)
        result = await self.session.execute(stmp)
        objects = result.scalars().all()
        if not objects:
            return {'message': 'Не удалось найти обьект по указанным полям!'}

        return {'message': 'Удаление успешно!'}
