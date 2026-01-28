from src.repositories.school_repository import SchoolRepository

class GetSchoolsUseCase:
    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    async def execute(self, page: int, per_page: int):
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
