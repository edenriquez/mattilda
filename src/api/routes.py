from flask_openapi3 import APIBlueprint, Tag
from src.schemas.schemas import SchoolCreate, SchoolResponse, SchoolEnvelope
from src.services.services import SchoolService
from typing import List

school_tag = Tag(name="School", description="School management")

school_router = APIBlueprint("school", __name__, url_prefix="/api/schools", abp_tags=[school_tag])


@school_router.post("/", responses={"201": SchoolResponse})
async def create_school(body: SchoolCreate):
    school = await SchoolService.create_school(body.name)
    return school.dict(), 201

@school_router.get("/", responses={"200": SchoolEnvelope})
async def get_schools():
    schools = await SchoolService.get_schools()
    envelope = SchoolEnvelope(data=schools)
    return envelope.dict(), 200
