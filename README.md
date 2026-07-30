# kirtuclub-downloader

A Python toolkit for downloading, merging, and OCR-processing PDF files from KirtuClub.

> **Downloaded PDFs are not stored in the repo.** Grab sample assets from the
> [Releases page](https://github.com/chirag127/kirtuclub-downloader/releases),
> or run the downloader to fetch your own.

## Overview

`kirtuclub-downloader` is a collection of Python utilities that automate the workflow of fetching scanned comic pages from KirtuClub, merging them into full PDF episodes, and running OCR to produce searchable PDFs. The project includes:

- **Image downloader** — fetches individual page images from KirtuClub and saves them in episode directories.
- **PDF merger** — combines multiple page-level PDFs into a single per-episode PDF file.
- **OCR batch processor** — runs `ocrmypdf` to add searchable text layers to scanned PDFs.

## Project Structure

```
kirtuclub-downloader/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   ├── download_images.py    # Download page images from KirtuClub
│   ├── merge_pdfs.py         # Merge page PDFs into per-episode PDF
│   ├── ocr_batch.py          # Batch OCR processing on scanned PDFs
│   └── utils.py              # Shared utility (HTTP download helper)
└── tests/
    ├── test_utils.py         # Tests for utility functions
    └── test_merge_pdfs.py    # Tests for PDF merging
```

The `content/` directory (created by the scripts) is git-ignored.

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
