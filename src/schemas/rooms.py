from typing import Annotated

from pydantic import BaseModel, Field

class RoomSchema(BaseModel):
    hotel_id: int
    title: str
    description: Annotated[str | None, Field(None)]
    price: int
    quantity: int

class CreateRoomSchema(RoomSchema):
    id: int


class RoomPATCH(BaseModel):
    hotel_id: Annotated[int | None, Field(None)]
    title: Annotated[str | None, Field(None)]
    description: Annotated[str | None, Field(None)]
    price: Annotated[int | None, Field(None)]
    quantity: Annotated[int | None, Field(None)]
