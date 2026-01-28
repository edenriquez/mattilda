from src.db import db
from src.schemas.schemas import Statement

class SchoolStatementRepository:
    @staticmethod
    async def _ensure_db():
        if not db.is_connected():
            await db.connect()

    async def find_with_statement(self, school_id: int):
        await self._ensure_db()
        try:
            school = await db.schools.find_unique(
                where={'id': school_id},
                include={'students': {'include': {'invoices': True}}}
            )
            if not school:
                return None
            
            total_billed = 0
            total_paid = 0
            total_unpaid = 0
            
            for student in school.students:
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