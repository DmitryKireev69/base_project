from pydantic import BaseModel, Field
from typing import Annotated


class HotelSchema(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: Annotated[str | None, Field(None)]
    location: Annotated[str | None, Field(None)]
