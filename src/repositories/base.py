from pydantic import BaseModel
from sqlalchemy import select, delete, update, insert


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        """Получение обьектов по фильтрам"""
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_one_or_none(self, **data):
        """Получение одного элемента по фильтрам"""
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item is None:
            return {'detail': 'Обьект с указанными данными не найден!'}

        return self.schema.model_validate(item, from_attributes=True)

    async def add(self, data: BaseModel):
        """Добавление нового обьекта"""
        stmp = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmp)
        item = result.scalars().one()
        return self.schema.model_validate(item, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        """Изменение обьекта"""
        stmp = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmp)
        items = result.scalars().all()
        if not items:
            return {'message': 'Не удалось найти обьект по указанным полям!'}

        return [self.schema.model_validate(item, from_attributes=True) for item in items]


    async def delete(self, **filter_by):
        """Удаление обьекта"""
        stmp = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmp)
        items = result.scalars().all()
        if not items:
            return {'message': 'Не удалось найти обьект по указанным полям!'}

        return [self.schema.model_validate(item, from_attributes=True) for item in items]
