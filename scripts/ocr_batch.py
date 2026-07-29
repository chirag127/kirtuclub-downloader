import argparse
import glob
import os
import random
import subprocess
import traceback

from PyPDF2 import PdfReader

TEXT_THRESHOLD = 50


def needs_ocr(path, threshold=TEXT_THRESHOLD):
    if "_ocr" in path or "all_in_one" in path:
        return False
    ocr_path = path.replace(".pdf", "_ocr.pdf")
    if os.path.exists(ocr_path):
        return False
    reader = PdfReader(path)
    total = len(reader.pages)
    sample_size = min(total, 10)
    pages = random.sample(range(total), sample_size) if total > 10 else range(total)
    text = ""
    for i in pages:
        try:
            text += reader.pages[i].extract_text()
        except Exception:
            return None
    return len(text) / sample_size < threshold


def run_ocr(pdf_path):
    ocr_path = pdf_path.replace(".pdf", "_ocr.pdf")
    result = subprocess.run(
        ["ocrmypdf", "-l", "eng", "--force-ocr", pdf_path, ocr_path],
        capture_output=True, text=True,
    )
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Batch OCR scanned PDFs")
    parser.add_argument("--root", default="content/savita-bhabhi/episode-01-to-57", help="Root directory to scan")
    parser.add_argument("--threshold", type=int, default=TEXT_THRESHOLD, help="Chars per page threshold")
    parser.add_argument("--force", action="store_true", help="OCR even if already detected")
    args = parser.parse_args()

    pdfs = sorted(glob.glob(os.path.join(args.root, "**", "*.pdf"), recursive=True))

    for pdf in pdfs:
        try:
            if args.force or needs_ocr(pdf, args.threshold):
                run_ocr(pdf)
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
