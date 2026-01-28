from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    school_id: int

class StudentUpdate(StudentBase):
    pass

class StudentPath(BaseModel):
    student_id: int = Field(..., description="The ID of the student")

class StudentResponse(StudentBase):
    id: int
    school_id: int
    name: str
    createdAt: datetime

class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(SchoolBase):
    pass

class SchoolPath(BaseModel):
    school_id: int = Field(..., description="The ID of the school")

class SchoolResponse(SchoolBase):
    id: int
    createdAt: datetime

class InvoiceBase(BaseModel):
    name: str
    amount: int
    paid: bool
    student_id: int

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[int] = None
    paid: Optional[bool] = None
    student_id: Optional[int] = None

class InvoicePath(BaseModel):
    invoice_id: int = Field(..., description="The ID of the invoice")

class InvoiceResponse(InvoiceBase):
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

class StudentEnvelope(BaseModel):
    data: List[StudentResponse]
    pagination: Pagination

class InvoiceEnvelope(BaseModel):
    data: List[InvoiceResponse]
    pagination: Pagination

# TODO: implement this
class SchoolWithStudentsResponse(SchoolResponse):
    students: List[StudentResponse]

class Statement(BaseModel):
    total_billed: int
    total_paid: int
    total_unpaid: int

class SchoolStatementResponse(BaseModel):
    school: SchoolResponse
    statement: Statement
    invoices: List[InvoiceResponse]

class StudentStatementResponse(BaseModel):
    student: StudentResponse
    statement: Statement
    invoices: List[InvoiceResponse]
