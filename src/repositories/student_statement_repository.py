from src.db import db
from src.schemas.schemas import Statement

class StudentStatementRepository:
    @staticmethod
    async def _ensure_db():
        if not db.is_connected():
            await db.connect()

    async def find_with_statement(self, student_id: int):
        await self._ensure_db()
        try:
            student = await db.students.find_unique(
                where={'id': student_id},
                include={'invoices': True}
            )
            if not student:
                return None
            
            total_billed = 0
            total_paid = 0
            total_unpaid = 0
            
            for invoice in student.invoices:
                total_billed += invoice.amount
                if invoice.paid:
                    total_paid += invoice.amount
                else:
                    total_unpaid += invoice.amount
            
            return Statement(
                total_billed=total_billed,
                total_paid=total_paid,
                total_unpaid=total_unpaid
            )
        finally:
            await db.disconnect()
