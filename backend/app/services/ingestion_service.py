from app.services.pdf_loader import extract_text_from_pdf
from app.services.document_loader import split_text_into_chunks
from app.services.vector_store import add_chunks_to_vector_store


def ingest_pdf(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)

    chunks = split_text_into_chunks(text)

    result = add_chunks_to_vector_store(chunks)

    return {
        "message": "PDF ingested successfully",
        "pdf_path": pdf_path,
        "chunks_created": len(chunks),
        "vector_store_result": result
    }