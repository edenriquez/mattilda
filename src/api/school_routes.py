from flask_openapi3 import APIBlueprint, Tag
from src.repositories.school_repository import SchoolRepository
from src.repositories.school_statement_repository import SchoolStatementRepository
from src.repositories.invoice_repository import InvoiceRepository
from src.schemas.schemas import SchoolCreate, SchoolResponse, SchoolEnvelope, PaginationParams, SchoolUpdate, SchoolPath, SchoolStatementResponse, Statement, InvoiceResponse
from src.use_cases.school_use_cases import CreateSchoolUseCase, GetSchoolsUseCase, UpdateSchoolUseCase, DeleteSchoolUseCase, GetSchoolStatementUseCase
from typing import List

school_tag = Tag(name="School", description="School management")
school_repository = SchoolRepository()
school_statement_repository = SchoolStatementRepository()
invoice_repository = InvoiceRepository()

school_router = APIBlueprint("school", __name__, url_prefix="/api/schools", abp_tags=[school_tag])


@school_router.post("/", responses={"201": SchoolResponse})
async def create_school(body: SchoolCreate):
    use_case = CreateSchoolUseCase(school_repository)
    school = await use_case.execute(body.name)
    return SchoolResponse(
        id=school.id,
        name=school.name,
        createdAt=school.createdAt
    ).dict(), 201

@school_router.get("/", responses={"200": SchoolEnvelope})
async def get_schools(query: PaginationParams):
    use_case = GetSchoolsUseCase(school_repository)
    schools, pagination = await use_case.execute(page=query.page, per_page=query.per_page)
    
    return SchoolEnvelope(
        data=[SchoolResponse(
            id=s.id,
            name=s.name,
            createdAt=s.createdAt
        ) for s in schools],
        pagination=pagination
    ).dict(), 200

@school_router.patch("/<int:school_id>", responses={"200": SchoolResponse})  
async def update_school(path: SchoolPath, body: SchoolUpdate):
    use_case = UpdateSchoolUseCase(school_repository)
    school = await use_case.execute(path.school_id, body.name)
    return SchoolResponse(
        id=school.id,
        name=school.name,
        createdAt=school.createdAt
    ).dict(), 200


@school_router.delete("/<int:school_id>", responses={"200": SchoolResponse})
async def delete_school(path: SchoolPath):
    use_case = DeleteSchoolUseCase(school_repository)
    school = await use_case.execute(path.school_id)
    return SchoolResponse(
        id=school.id,
        name=school.name,
        createdAt=school.createdAt
    ).dict(), 200


@school_router.get("/<int:school_id>/statement", responses={"200": SchoolStatementResponse})
async def get_school_statement(path: SchoolPath):
    use_case = GetSchoolStatementUseCase(school_repository, school_statement_repository, invoice_repository)
    school, statement, invoices = await use_case.execute(path.school_id)
    
    if not school:
        return {"error": "School not found"}, 404
        
    return SchoolStatementResponse(
        school=SchoolResponse(
            id=school.id,
            name=school.name,
            createdAt=school.createdAt
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