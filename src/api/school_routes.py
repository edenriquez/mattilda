from flask_openapi3 import APIBlueprint, Tag
from src.schemas.schemas import SchoolCreate, SchoolResponse, SchoolEnvelope, PaginationParams
from src.repositories.school_repository import SchoolRepository
from src.use_cases.school_use_cases import CreateSchoolUseCase, GetSchoolsUseCase
from typing import List

school_tag = Tag(name="School", description="School management")
school_repository = SchoolRepository()

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
