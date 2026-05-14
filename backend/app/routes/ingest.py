import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.services.pdf_loader import extract_text_from_pdf
from app.services.document_loader import split_text_into_chunks
from app.services.embedding_service import create_embeddings
from app.services.vector_store import add_chunks_to_vectorstore

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/ingest-pdf")
async def ingest_pdf(files: List[UploadFile] = File(...)):
    try:
        total_chunks = 0
        processed_files = []

        for file in files:
            if not file.filename.endswith(".pdf"):
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} is not a PDF file."
                )

            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            text = extract_text_from_pdf(file_path)
            chunks = split_text_into_chunks(text)

            embeddings = create_embeddings(chunks)

            add_chunks_to_vectorstore(
                chunks=chunks,
                embeddings=embeddings,
                source=file.filename
            )

            total_chunks += len(chunks)
            processed_files.append(file.filename)

        return {
            "message": "PDFs ingested successfully",
            "files": processed_files,
            "total_chunks": total_chunks
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )