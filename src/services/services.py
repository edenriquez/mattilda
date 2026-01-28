from src.db import db

class SchoolService:
    @staticmethod
    async def create_school(name):
        if not db.is_connected():
            await db.connect()
        try:
            return await db.schools.create(
                data={
                    'name': name,
                }
            )
        finally:
            await db.disconnect()

    @staticmethod
    async def find_one(school_id):
        if not db.is_connected():
            await db.connect()
        try:
            return await db.schools.find_unique(where={'id': school_id})
        finally:
            await db.disconnect()

    @staticmethod
    async def get_schools():
        if not db.is_connected():
            await db.connect()
        try:
            return await db.schools.find_many()
        finally:
            await db.disconnect()

