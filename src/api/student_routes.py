from flask_openapi3 import APIBlueprint, Tag
from src.schemas.schemas import StudentCreate, StudentResponse, StudentEnvelope, PaginationParams, StudentPath, StudentUpdate, StudentStatementResponse, Statement, InvoiceResponse
from src.repositories.student_repository import StudentRepository
from src.repositories.student_statement_repository import StudentStatementRepository
from src.repositories.invoice_repository import InvoiceRepository
from src.use_cases.student_use_cases import CreateStudentUseCase, GetStudentsUseCase, UpdateStudentUseCase, DeleteStudentUseCase, GetStudentStatementUseCase
from typing import List

student_tag = Tag(name="Student", description="Student management")
student_repository = StudentRepository()
student_statement_repository = StudentStatementRepository()
invoice_repository = InvoiceRepository()

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

@student_router.patch("/<int:student_id>", responses={"200": StudentResponse})
async def update_student(path: StudentPath, body: StudentUpdate):
    use_case = UpdateStudentUseCase(student_repository)
    student = await use_case.execute(path.student_id, body.name)
    return StudentResponse(
        id=student.id,
        name=student.name,
        school_id=student.schoolId,
        createdAt=student.createdAt
    ).dict(), 200

@student_router.delete("/<int:student_id>", responses={"200": StudentResponse})
async def delete_student(path: StudentPath):
    use_case = DeleteStudentUseCase(student_repository)
    student = await use_case.execute(path.student_id)
    return StudentResponse(
        id=student.id,
        name=student.name,
        school_id=student.schoolId,
        createdAt=student.createdAt
    ).dict(), 200

@student_router.get("/<int:student_id>/statement", responses={"200": StudentStatementResponse})
async def get_student_statement(path: StudentPath):
    use_case = GetStudentStatementUseCase(student_repository, student_statement_repository, invoice_repository)
    student, statement, invoices = await use_case.execute(path.student_id)
    
    if not student:
        return {"error": "Student not found"}, 404
        
    return StudentStatementResponse(
        student=StudentResponse(
            id=student.id,
            name=student.name,
            school_id=student.schoolId,
            createdAt=student.createdAt
        ),
        statement=Statement(
            total_billed=statement.total_billed,
            total_paid=statement.total_paid,
            total_unpaid=statement.total_unpaid
        ),
        invoices=[InvoiceResponse(
            id=i.id,
            name=i.name,
            amount=i.amount,
            paid=i.paid,
            student_id=i.studentId,
            createdAt=i.createdAt
        ) for i in invoices]
    ).dict(), 200