from fastapi import APIRouter, Response
from src.schemas.users import CreateUserSchema, AuthUserSchema
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.routers.dependencies import UserIdDep
router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и аутентификация"],
)


@router.post('/register', summary='Регистрация пользователя')
async def register_user(user_data: CreateUserSchema):
    """Регистрация пользователя"""
    async with async_session_maker() as session:
        await UsersRepository(session).add(user_data)
        await session.commit()
        return {'detail': 'Пользователь создан'}

@router.post('/login', summary='Аутентификация пользователя')
async def login_user(user_data: AuthUserSchema, response: Response):
    """Аутентификация пользователя"""
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_password(email=user_data.email)
        if not AuthService.verify_password(user_data.password, user.password):
            return {'detail': 'Пароль не верный!'}

        access_token = AuthService.create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}

@router.get('/get_me', summary='Текущий пользователь')
async def only_auth(user_id: UserIdDep):
    """Проверяем текущего пользователя"""
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        if not user:
            return {'detail': 'Пользователь не найден!'}
        return user
