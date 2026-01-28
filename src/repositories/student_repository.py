from src.db import db

class StudentRepository:
    @staticmethod
    async def _ensure_db():
        if not db.is_connected():
            await db.connect()

    async def create(self, name: str, school_id: int):
        await self._ensure_db()
        try:
            return await db.students.create(data={'name': name, 'schoolId': school_id})
        finally:
            await db.disconnect()

    async def find_many(self, skip: int, take: int):
        await self._ensure_db()
        try:
            return await db.students.find_many(
                skip=skip,
                take=take,
                order={'createdAt': 'desc'}
            )
        finally:
            await db.disconnect()

    async def find_by_id(self, student_id: int):
        await self._ensure_db()
        try:
            return await db.students.find_unique(where={'id': student_id})
        finally:
            await db.disconnect()
    
    async def count(self):
        await self._ensure_db()
        try:
            return await db.students.count()
        finally:
            await db.disconnect()
