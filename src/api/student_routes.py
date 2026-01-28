from flask_openapi3 import APIBlueprint, Tag
from src.schemas.schemas import StudentCreate, StudentResponse, StudentEnvelope, PaginationParams
from src.repositories.student_repository import StudentRepository
from src.use_cases.student_use_cases import CreateStudentUseCase, GetStudentsUseCase
from typing import List

student_tag = Tag(name="Student", description="Student management")
student_repository = StudentRepository()

student_router = APIBlueprint("student", __name__, url_prefix="/api/students", abp_tags=[student_tag])


@student_router.post("/", responses={"201": StudentResponse})
async def create_student(body: StudentCreate):
    # NOTE: validate param presence for now, later we should query db to validat school exists
    if not body.school_id:
        return {"error": "School ID is required"}, 400

    use_case = CreateStudentUseCase(student_repository)
    student = await use_case.execute(name=body.name, school_id=body.school_id)
    
    return StudentResponse(
        id=student.id,
        name=student.name,
        school_id=student.schoolId,
        createdAt=student.createdAt
    ).dict(), 201

@student_router.get("/", responses={"200": StudentEnvelope})
async def get_students(query: PaginationParams):
    use_case = GetStudentsUseCase(student_repository)
    students, pagination = await use_case.execute(page=query.page, per_page=query.per_page)
    
    return StudentEnvelope(
        data=[
            StudentResponse(
                id=s.id,
                name=s.name,
                school_id=s.schoolId,
                createdAt=s.createdAt
            ) for s in students
        ],
        pagination=pagination
    ).dict(), 200
