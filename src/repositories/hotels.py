from sqlalchemy import select
from src.models import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, limit, offset, title, location):
        query = select(self.model)
        if title:
            query = query.where(HotelsOrm.title.ilike(f'%{title.strip()}%'))
        if location:
            query = query.where(HotelsOrm.location.ilike(f'%{location.strip()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
