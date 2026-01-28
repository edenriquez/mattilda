from src.db import db

class SchoolRepository:
    @staticmethod
    async def _ensure_db():
        if not db.is_connected():
            await db.connect()

    async def create(self, name: str):
        await self._ensure_db()
        try:
            return await db.schools.create(data={'name': name})
        finally:
            await db.disconnect()

    async def find_many(self, skip: int, take: int):
        await self._ensure_db()
        try:
            return await db.schools.find_many(
                skip=skip,
                take=take,
                order={'createdAt': 'desc'}
            )
        finally:
            await db.disconnect()

    async def find_by_id(self, school_id: int):
        await self._ensure_db()
        try:
            return await db.schools.find_unique(where={'id': school_id})
        finally:
            await db.disconnect()
            
    async def count(self):  
        await self._ensure_db()
        try:
            return await db.schools.count()
        finally:
            await db.disconnect()

    async def update(self, school_id: int, name: str):
        await self._ensure_db()
        try:
            return await db.schools.update(
                where={'id': school_id},
                data={'name': name}
            )
        finally:
            await db.disconnect()

    async def delete(self, school_id: int):
        await self._ensure_db()
        try:
            return await db.schools.delete(where={'id': school_id})
        finally:
            await db.disconnect()