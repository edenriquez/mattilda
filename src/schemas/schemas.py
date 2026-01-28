from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class SchoolResponse(SchoolBase):
    id: int
    createdAt: datetime

class SchoolEnvelope(BaseModel):
    data: List[SchoolResponse]