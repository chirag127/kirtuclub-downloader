# private-pdf-download

A Python toolkit for downloading, merging, and OCR-processing PDF files — originally built for batch-downloading and processing Savita Bhabhi comic episodes from KirtuClub.

## Overview

`private-pdf-download` is a collection of Python utilities that automate the workflow of fetching scanned comic pages from a web source, merging them into full PDF episodes, and running OCR to produce searchable PDFs. The project includes:

- **Image downloader** — fetches individual page images from a remote source and saves them in episode directories.
- **PDF merger** — combines multiple page-level PDFs into a single per-episode PDF file.
- **OCR batch processor** — runs `ocrmypdf` to add searchable text layers to scanned PDFs.

## Project Structure

```
private-pdf-download/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   ├── download_images.py    # Download page images from remote source
│   ├── merge_pdfs.py         # Merge page PDFs into per-episode PDFs
│   ├── ocr_batch.py          # Batch OCR processing on scanned PDFs
│   └── utils.py              # Shared utility (HTTP download helper)
└── content/
    └── savita-bhabhi/
        ├── episode-01-to-57/   # 57 episodes (original + OCR PDFs)
        └── images/
            └── episode-153/    # Sample downloaded page images
```

## Requirements

- Python 3.10+
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [requests](https://pypi.org/project/requests/)
- [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) (for OCR functionality)

## Usage

### Download images

```bash
python scripts/download_images.py
```

### Merge PDFs

```bash
python scripts/merge_pdfs.py
```

### Run OCR batch

```bash
python scripts/ocr_batch.py
```

## License

This project is licensed under the [MIT License](LICENSE).