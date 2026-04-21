from typing import Annotated
from fastapi import Query, Depends, Request, HTTPException, status
from pydantic import BaseModel
from src.services.auth import AuthService

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, description='Страница'),]
    per_page: Annotated[int, Query(5, lt=30, description='Количество элементов на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    """Получение токена"""
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не предоставили токен доступа!')
    return access_token

def get_current_user_id(access_token: str = Depends(get_token)) -> int:
    """Получение идентификатора пользователя по токену"""
    data = AuthService.decode_token(access_token)
    user_id = data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Идентификатор пользователя не найден в токене!')
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
