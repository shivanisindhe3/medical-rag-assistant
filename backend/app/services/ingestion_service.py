import os

from app.services.pdf_loader import extract_text_from_pdf
from app.services.document_loader import split_text_into_chunks
from app.services.embedding_service import create_embeddings
from app.services.vector_store import add_chunks_to_vectorstore


def ingest_pdf(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)

    chunks = split_text_into_chunks(text)

    embeddings = create_embeddings(chunks)

    source = os.path.basename(pdf_path)

    result = add_chunks_to_vectorstore(
        chunks=chunks,
        embeddings=embeddings,
        source=source
    )

    return {
        "message": "PDF ingested successfully",
        "pdf_path": pdf_path,
        "source": source,
        "chunks_created": len(chunks),
        "vector_store_result": result
    }