from typing import Any
from docx import Document
from pypdf import PdfReader
from pathlib import Path
import logging


CHUNK_SIZE = 300
OVERLAP = 50

logger = logging.getLogger(__name__)


def extract_text_from_pdf(path: Path) -> str:
    try:
        doc: PdfReader = PdfReader(path)
        return "\n".join(page.extract_text() for page in doc.pages)
    except Exception as e:
        logger.warning(f"Invalid PDF: {path.name} — {e}")
        return ""


def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def load_documents(folder_path: str):
    """
    Load and chunk documents from a folder.
    Returns a list of dicts with: text, source, chunk_id
    """
    chunks = []
    text = ""

    for file in Path(folder_path).glob("*"):
        try:
            if file.suffix.lower() == ".pdf":
                text = extract_text_from_pdf(file)
            elif file.suffix.lower() == ".docx":
                text = extract_text_from_docx(str(file))
            else:
                continue
            file_chunks = chunk_text(text, file.name)
            chunks.extend(file_chunks)

        except Exception as e:
            logger.error(f"Failed to process file: {file} - {e}")
            continue

    return chunks


def chunk_text(text: str, source: str) -> list[dict[str, Any]]:
    chunks = []
    start = 0
    chunk_id = 0
    try:
        while start < len(text):
            end = min(start + CHUNK_SIZE, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {"text": chunk_text, "source": source, "chunk_id": chunk_id}
                )
                chunk_id += 1
            start += CHUNK_SIZE - OVERLAP

    except Exception as e:
        logger.error(f"Error while chunking text from {source}: {e}")
        raise RuntimeError(f"Failed to chunk document: {source}") from e
    return chunks
