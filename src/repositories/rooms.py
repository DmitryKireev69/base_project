from src.models import RoomOrm
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomOrm
