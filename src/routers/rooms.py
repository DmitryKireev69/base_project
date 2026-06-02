from fastapi import APIRouter, status

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomSchema, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms", summary='Получение номеров',
            status_code=status.HTTP_200_OK)
async def get_rooms(hotel_id: int):
    """Получение номеров"""
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.post('/rooms', summary='Создать номер в отеле',
             status_code=status.HTTP_201_CREATED)
async def create_room(room_data: RoomSchema):
    """Создание номера в отеле"""
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
        return room


@router.delete('/{hotel_id}/{room_id}', summary='Удаление номера в отеле',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(hotel_id: int, room_id: int):
    """Удаление номера в отеле"""
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()


@router.put('{hotel_id}/{room_id}', summary='Полное обновление номера',
            status_code=status.HTTP_200_OK)
async def update_room(hotel_id: int, room_id: int, room_data: RoomSchema):
    """Полное обновление данных номера"""
    async with async_session_maker() as session:
        result = await RoomsRepository(
            session
        ).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return result


@router.patch('{hotel_id}/{room_id}', summary='Частичное обновление номера', status_code=status.HTTP_200_OK)
async def update_room(hotel_id: int, room_id: int, room_data: RoomPATCH):
    """Частичное обновление номера"""
    async with async_session_maker() as session:
        result = await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return result
