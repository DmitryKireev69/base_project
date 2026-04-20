from pydantic import BaseModel
from src.repositories.base import BaseRepository
from src.models import UserOrm
from src.schemas.users import UserSchema, AuthUserWithIdAndPassword
from sqlalchemy import insert, select
from src.services.auth import AuthService

class UsersRepository(BaseRepository):
    model = UserOrm
    schema = UserSchema


    async def add(self, user_data: BaseModel):
        """Создание пользователя"""
        user_d = user_data.model_dump()
        user_d['password'] = AuthService().hash_password(user_d['password'])
        stmp = insert(self.model).values(**user_d)
        await self.session.execute(stmp)

    async def get_one_or_none(self, **data):
        """Получение одного элемента по фильтрам"""
        query = select(self.model).filter_by(**data)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        if user is None:
            return {'detail': 'Отеля с указанным идентификатором не найдено!'}

        return AuthUserWithIdAndPassword.model_validate(user, from_attributes=True)

