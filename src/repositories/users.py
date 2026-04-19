from datetime import datetime, timezone, timedelta

from pydantic import BaseModel
from src.repositories.base import BaseRepository
from src.models import UserOrm
from src.schemas.users import UserSchema, AuthUserWithIdAndPassword
from sqlalchemy import insert, select
from passlib.context import CryptContext
import jwt

class UsersRepository(BaseRepository):
    model = UserOrm
    schema = UserSchema
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    async def add(self, user_data: BaseModel):
        """Создание пользователя"""
        user_d = user_data.model_dump()
        user_d['password'] = self.hash_password(user_d['password'])
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

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Проверяет, соответствует ли пароль хешу"""
        return cls.pwd_context.verify(plain_password, hashed_password)