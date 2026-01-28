from src.repositories.invoice_repository import InvoiceRepository

class GetInvoicesUseCase:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    async def execute(self, page: int = 1, per_page: int = 10):
        skip = (page - 1) * per_page
        
        total = await self.repository.count()
        invoices = await self.repository.find_many(skip=skip, take=per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return invoices, {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages
        }

class CreateInvoiceUseCase:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    async def execute(self, name: str, amount: int, student_id: int):
        return await self.repository.create(name, amount, student_id)


class UpdateInvoiceUseCase:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    async def execute(self, id: int, data: dict):
        return await self.repository.update(id, data)

class DeleteInvoiceUseCase:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    async def execute(self, id: int):
        return await self.repository.delete(id)
