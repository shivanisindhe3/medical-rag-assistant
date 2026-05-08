from fastapi import APIRouter

from app.schemas.ingest import PDFIngestRequest
from app.services.ingestion_service import ingest_pdf

router = APIRouter()


@router.post("/ingest-pdf")
def ingest_pdf_endpoint(request: PDFIngestRequest):
    result = ingest_pdf(request.pdf_path)
    return result