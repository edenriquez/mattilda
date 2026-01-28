from src.db import db

class InvoiceRepository:
    @staticmethod
    async def _ensure_db():
        if not db.is_connected():
            await db.connect()

    async def create(self, name: str, amount: int, student_id: int):
        await self._ensure_db()
        try:
            return await db.invoices.create(data={'name': name, 'amount': amount, 'studentId': student_id})
        finally:
            await db.disconnect()

    async def find_many(self, skip: int, take: int):
        await self._ensure_db()
        try:
            return await db.invoices.find_many(
                skip=skip,
                take=take,
                order={'createdAt': 'desc'}
            )
        finally:
            await db.disconnect()

    async def find_by_id(self, invoice_id: int):
        await self._ensure_db()
        try:
            return await db.invoices.find_unique(where={'id': invoice_id})
        finally:
            await db.disconnect()
            
    async def count(self):  
        await self._ensure_db()
        try:
            return await db.invoices.count()
        finally:
            await db.disconnect()

    async def update(self, invoice_id: int, data: dict):
        await self._ensure_db()
        if 'student_id' in data:
            data['studentId'] = data.pop('student_id')
            
        try:
            return await db.invoices.update(
                where={'id': invoice_id},
                data=data
            )
        finally:
            await db.disconnect()

    async def delete(self, invoice_id: int):
        await self._ensure_db()
        try:
            return await db.invoices.delete(where={'id': invoice_id})
        finally:
            await db.disconnect()

    async def find_by_school(self, school_id: int):
        await self._ensure_db()
        try:
            return await db.invoices.find_many(
                where={'student': {'schoolId': school_id}},
            )
        finally:
            await db.disconnect()

    async def find_by_student(self, student_id: int):
        await self._ensure_db()
        try:
            return await db.invoices.find_many(
                where={'studentId': student_id}
            )
        finally:
            await db.disconnect()