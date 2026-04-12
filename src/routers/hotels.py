from fastapi import Query, Path, status, APIRouter, Body
from src.schemas.hotels import HotelSchema, HotelPATCH
from src.models.hotels import HotelsOrm
from src.database import async_session_maker
from sqlalchemy import insert, select, delete, update
from src.schemas.dependencies import PaginationDep

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

@router.get("", summary='Получение отелей', status_code=status.HTTP_200_OK)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description='Название отеля'),
        location: str | None = Query(None, description='Локация отеля')
):
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.ilike(f'%{title.strip()}%'))
        if location:
            query = query.where(HotelsOrm.location.ilike(f'%{location.strip()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(query)
        return result.scalars().all()


@router.delete("/{hotel_id}", summary='Удаление отеля', status_code=status.HTTP_200_OK)
async def del_hotel(hotel_id: int = Path(description='Идентификатор отеля')):
    async with async_session_maker() as session:
        stmp = select(HotelsOrm).filter_by(id=hotel_id)
        result = await session.scalars(stmp)
        hotel = result.one_or_none()
        if not hotel:
            return {'message': f'Отель с идентификатором {hotel_id} Не найден!'}
        await session.delete(hotel)
        await session.commit()
        return {'message': f'Отель с идентификатором {hotel_id} удален!'}

@router.post("", summary='Создание отеля', status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_data: HotelSchema = Body(
    openapi_examples={
        1 : {'summary': 'Сочи', 'value':{
        'title': 'Сочи у моря 5 звезд',
        'location': 'Улица пушкина, дом 6'
    }},
        2 : {'summary': 'Дубай', 'value':{
        'title': 'Сочи у моря 5 звезд',
        'location': 'Улица хулиганов, дом 8'
    }}
})):

    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'message': f'Создан новый отель {hotel_data.title}'}

@router.put('/{hotel_id}', summary='Обновление данных отеля', status_code=status.HTTP_200_OK)
async def update_hotel(
    hotel_data: HotelSchema,
    hotel_id: int = Path(description='Идентификатор отеля')
):
    async with async_session_maker() as session:
        stmp = update(HotelsOrm).filter_by(id=hotel_id).values(**hotel_data.model_dump())
        result = await session.execute(stmp)

        if result.rowcount == 0:
            return {'message': f'Отель с идентификатором {hotel_id} Не найден!'}
        await session.commit()

        return {f'message: Данные отеля {hotel_id} обновленны!'}


@router.patch('/{hotel_id}', summary='Обновление характеристики отеля', status_code=status.HTTP_200_OK)
def update_hotel_element(
        hotel_data: HotelPATCH,
        hotel_id: int = Path(),

):
    if hotel_data.title is None and hotel_data.name is None:
        return {'message': 'Вы не передали параметры на изменение!'}

    hotel = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel:
        return {'message': f'Отеля с указанным идентификатором {hotel_id} не найдено'}

    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {'message': f'Данные отеля {hotel['title']} изменены!'}
