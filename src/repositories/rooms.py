from src.models import RoomOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    model = RoomOrm
    schema = RoomSchema
