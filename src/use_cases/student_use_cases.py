from src.repositories.student_repository import StudentRepository

class CreateStudentUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def execute(self, name: str, school_id: int):
        return await self.repository.create(name=name, school_id=school_id)

class GetStudentsUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def execute(self, page: int, per_page: int):
        skip = (page - 1) * per_page
        
        total = await self.repository.count()
        students = await self.repository.find_many(skip=skip, take=per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return students, {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages
        }

class UpdateStudentUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def execute(self, student_id: int, name: str):
        return await self.repository.update(student_id=student_id, name=name)

class DeleteStudentUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def execute(self, student_id: int):
        return await self.repository.delete(student_id=student_id)
