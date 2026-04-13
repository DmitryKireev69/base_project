from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class HotelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    location: str


class HotelResponseSchema(BaseModel):
    status: str
    data: HotelSchema

class HotelPATCH(BaseModel):
    title: Annotated[str | None, Field(None)]
    location: Annotated[str | None, Field(None)]
