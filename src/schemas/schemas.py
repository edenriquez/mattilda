from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")

class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int
    createdAt: datetime

class Pagination(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int

class SchoolEnvelope(BaseModel):
    data: List[SchoolResponse]
    pagination: Pagination
