from flask_openapi3 import APIBlueprint, Tag
from src.schemas.schemas import InvoiceCreate, InvoiceResponse, InvoiceEnvelope, PaginationParams, InvoiceUpdate, InvoicePath
from src.repositories.invoice_repository import InvoiceRepository
from src.use_cases.invoice_use_cases import CreateInvoiceUseCase, GetInvoicesUseCase, UpdateInvoiceUseCase, DeleteInvoiceUseCase
from typing import List

invoice_tag = Tag(name="Invoice", description="Invoice management")
invoice_repository = InvoiceRepository()

invoice_router = APIBlueprint("invoice", __name__, url_prefix="/api/invoices", abp_tags=[invoice_tag])


@invoice_router.post("/", responses={"201": InvoiceResponse})
async def create_invoice(body: InvoiceCreate):
    use_case = CreateInvoiceUseCase(invoice_repository)
    invoice = await use_case.execute(body.name, body.amount, body.student_id)
    
    # Debug: Print fields if error persists
    # print(f"DEBUG: Invoice fields: {invoice.dict().keys()}")
    
    return InvoiceResponse(
        id=invoice.id,
        name=invoice.name,
        amount=invoice.amount,
        student_id=invoice.studentId,
        createdAt=invoice.createdAt
    ).dict(), 201

@invoice_router.get("/", responses={"200": InvoiceEnvelope})
async def get_invoices(query: PaginationParams):
    use_case = GetInvoicesUseCase(invoice_repository)
    invoices, pagination = await use_case.execute(page=query.page, per_page=query.per_page)
    
    return InvoiceEnvelope(
        data=[InvoiceResponse(
            id=i.id,
            name=i.name,
            amount=i.amount,
            student_id=i.studentId,
            createdAt=i.createdAt
        ) for i in invoices],
        pagination=pagination
    ).dict(), 200

@invoice_router.patch("/<int:invoice_id>", responses={"200": InvoiceResponse})  
async def update_invoice(path: InvoicePath, body: InvoiceUpdate):
    use_case = UpdateInvoiceUseCase(invoice_repository)
    invoice = await use_case.execute(path.invoice_id, body.name)
    return InvoiceResponse(
        id=invoice.id,
        name=invoice.name,
        createdAt=invoice.createdAt
    ).dict(), 200


@invoice_router.delete("/<int:invoice_id>", responses={"200": InvoiceResponse})
async def delete_invoice(path: InvoicePath):
    use_case = DeleteInvoiceUseCase(invoice_repository)
    invoice = await use_case.execute(path.invoice_id)
    return InvoiceResponse(
        id=invoice.id,
        name=invoice.name,
        createdAt=invoice.createdAt
    ).dict(), 200