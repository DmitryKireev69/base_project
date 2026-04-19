from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, description='Страница'),]
    per_page: Annotated[int, Query(5, lt=30, description='Количество элементов на странице')]


PaginationDep = Annotated[PaginationParams, Depends()]
