from fastapi import Query, Path, status, APIRouter, Body
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPATCH, CreateHotelSchema
from src.database import async_session_maker
from src.routers.dependencies import PaginationDep

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
        return await HotelsRepository(session).get_all(limit, offset, title, location)

@router.get('/{hotel_id}', summary="Получение отеля", status_code=status.HTTP_200_OK)
async def get_hotel(hotel_id: int = Path(description='Идентификатор отеля')):
    async with async_session_maker() as session:
            return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}", summary='Удаление отеля', status_code=status.HTTP_200_OK)
async def del_hotel(hotel_id: int = Path(description='Идентификатор отеля')):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return result

@router.post("", summary='Создание отеля', status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_data: CreateHotelSchema = Body(
    openapi_examples={
        1 : {'summary': 'Сочи', 'value':{
        'title': 'Сочи у моря 5 звезд',
        'location': 'Улица пушкина, дом 6'
    }},
        2 : {'summary': 'Дубай', 'value':{
        'title': 'Дубай у моря 5 звезд',
        'location': 'Улица хулиганов, дом 8'
    }}
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
        return hotel

@router.put('/{hotel_id}', summary='Обновление данных отеля', status_code=status.HTTP_200_OK)
async def update_hotel(
    hotel_data: CreateHotelSchema,
    hotel_id: int = Path(description='Идентификатор отеля'),
):
    async with async_session_maker() as session:
        res = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return res


@router.patch('/{hotel_id}', summary='Обновление характеристики отеля', status_code=status.HTTP_200_OK)
async def update_hotel_element(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        res = await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return res
