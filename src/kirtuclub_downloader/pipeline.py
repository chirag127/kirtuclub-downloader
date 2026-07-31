"""Pipeline stages: download → assemble → OCR → merge.

Each stage is a pure-ish function taking a :class:`Config` and explicit
paths, so the CLI and tests drive them the same way. No global state.
"""

from __future__ import annotations

import glob
import os
import subprocess

import img2pdf
from pypdf import PdfReader, PdfWriter

from .config import Config
from .http import Downloader


def download_episode(
    downloader: Downloader,
    config: Config,
    episode: int,
) -> list[str]:
    """Download every page image for one episode. Returns saved file paths.

    Stops at the first page that 404s (end of episode).
    """
    out_dir = os.path.join(
        config.content_dir, config.series, "images", f"episode-{episode:03d}"
    )
    os.makedirs(out_dir, exist_ok=True)
    saved: list[str] = []
    for page in range(1, config.max_pages + 1):
        url = (
            f"{config.base_url}/{config.series}-episode-"
            f"{episode}-{page}.jpg"
        )
        path = os.path.join(out_dir, f"{page:03d}.jpg")
        if os.path.exists(path):
            saved.append(path)
            continue
        data = downloader.fetch(url)
        if data is None:
            break
        with open(path, "wb") as fh:
            fh.write(data)
        saved.append(path)
    return saved


def images_to_pdf(image_paths: list[str], out_path: str) -> bool:
    """Combine page images (in sorted order) into one PDF. Skips if exists."""
    if os.path.exists(out_path):
        return True
    if not image_paths:
        return False
    ordered = sorted(image_paths)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(img2pdf.convert(ordered))
    return True


def _page_text_len(reader: PdfReader, sample: int) -> float:
    total = len(reader.pages)
    count = min(total, sample)
    text = ""
    for i in range(count):
        try:
            text += reader.pages[i].extract_text() or ""
        except Exception:
            return 0.0
    return len(text) / count if count else 0.0


def needs_ocr(pdf_path: str, config: Config) -> bool:
    """True if the PDF has little embedded text (i.e. scanned images)."""
    name = os.path.basename(pdf_path)
    if "_ocr" in name or "all_in_one" in name:
        return False
    if os.path.exists(pdf_path.replace(".pdf", "_ocr.pdf")):
        return False
    try:
        reader = PdfReader(pdf_path)
    except Exception:
        return True
    return _page_text_len(reader, 10) < config.text_threshold


def run_ocr(pdf_path: str, config: Config) -> bool:
    """Add a searchable text layer via ocrmypdf. Returns success."""
    ocr_path = pdf_path.replace(".pdf", "_ocr.pdf")
    result = subprocess.run(
        [
            "ocrmypdf", "-l", config.ocr_lang, "--force-ocr",
            pdf_path, ocr_path,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def merge_pdfs(pdfs: list[str], out_path: str, config: Config) -> bool:
    """Merge PDFs into one file, skipping outputs over the size cap."""
    if os.path.exists(out_path):
        return True
    writer = PdfWriter()
    for pdf in sorted(pdfs):
        try:
            writer.append(pdf)
        except Exception:
            continue
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    if size_mb > config.max_merge_mb:
        os.remove(out_path)
        return False
    return True


def find_pdfs(root: str, pattern: str = "*.pdf") -> list[str]:
    """Recursively find PDFs under ``root`` matching ``pattern``."""
    return sorted(glob.glob(os.path.join(root, "**", pattern), recursive=True))
