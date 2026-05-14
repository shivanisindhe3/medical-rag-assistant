import re
from pathlib import Path
from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text before chunking and embedding.
    """

    if not text:
        return ""

    # Remove repeated new lines and extra spaces
    text = re.sub(r"\s+", " ", text)

    # Fix words where letters are separated by spaces:
    # Example: "D i a b e t e s" -> "Diabetes"
    text = re.sub(r"\b(?:[A-Za-z]\s){2,}[A-Za-z]\b", lambda m: m.group(0).replace(" ", ""), text)

    # Fix common spacing around punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    # Remove extra spaces again
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and cleans text from a PDF file.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(str(path))
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            cleaned_page_text = clean_text(page_text)
            pages_text.append(cleaned_page_text)

    final_text = "\n\n".join(pages_text).strip()

    if not final_text:
        raise ValueError("No readable text found in the PDF.")

    return final_text