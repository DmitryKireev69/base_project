from http.client import HTTPException

from fastapi import APIRouter, Response
from src.schemas.users import CreateUserSchema, AuthUserSchema
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"],
)


@router.post('/register')
async def register_user(user_data: CreateUserSchema):
    async with async_session_maker() as session:
        await UsersRepository(session).add(user_data)
        await session.commit()
        return {'detail': 'Пользователь создан'}

@router.post('/login')
async def login_user(user_data: AuthUserSchema, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=user_data.email)
        if not UsersRepository.verify_password(user_data.password, user.password):
            return {'detail': 'Пароль не верный!'}

        access_token = UsersRepository.create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}
