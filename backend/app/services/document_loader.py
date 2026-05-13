from pathlib import Path


def load_text_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path.read_text(encoding="utf-8")


def split_text_into_chunks(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list[str]:
    if not text or not text.strip():
        return []

    chunks = []
    start = 0
    text = text.strip()

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks