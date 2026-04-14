from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class CreateHotelSchema(BaseModel):
    title: str
    location: str


class HotelSchema(CreateHotelSchema):
    id: int


class HotelPATCH(BaseModel):
    title: Annotated[str | None, Field(None)]
    location: Annotated[str | None, Field(None)]
