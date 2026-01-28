from src.repositories.school_repository import SchoolRepository
from src.repositories.school_statement_repository import SchoolStatementRepository
from src.repositories.invoice_repository import InvoiceRepository
from src.schemas.schemas import SchoolBase, Statement, InvoiceResponse

class GetSchoolsUseCase:
    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    async def execute(self, page: int = 1, per_page: int = 10):
        skip = (page - 1) * per_page
        
        total = await self.repository.count()
        schools = await self.repository.find_many(skip=skip, take=per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return schools, {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages
        }

class CreateSchoolUseCase:
    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    async def execute(self, name: str):
        return await self.repository.create(name)


class UpdateSchoolUseCase:
    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    async def execute(self, id: int, name: str):
        return await self.repository.update(id, name)

class DeleteSchoolUseCase:
    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    async def execute(self, id: int):
        return await self.repository.delete(id)


class GetSchoolStatementUseCase:
    def __init__(self, repository: SchoolRepository, statement_repository: SchoolStatementRepository, invoice_repository: InvoiceRepository):
        self.repository = repository
        self.statement_repository = statement_repository
        self.invoice_repository = invoice_repository

    async def execute(self, id: int):
        school = await self.repository.find_by_id(id)
        if not school:
            return None, None, None
            
        statement = await self.statement_repository.find_with_statement(id)
        invoices = await self.invoice_repository.find_by_school(id)
        
        return school, statement, invoices