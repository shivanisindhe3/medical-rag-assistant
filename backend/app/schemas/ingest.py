from pydantic import BaseModel


class PDFIngestRequest(BaseModel):
    pdf_path: str