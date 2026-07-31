# kirtuclub-downloader

[![CI](https://github.com/chirag127/kirtuclub-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/chirag127/kirtuclub-downloader/actions/workflows/ci.yml)
[![Stars](https://img.shields.io/github/stars/chirag127/kirtuclub-downloader?style=flat)](https://github.com/chirag127/kirtuclub-downloader/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

One CLI for the full comic-PDF workflow: **download → assemble → OCR → merge**.

> **Releases (sample assets):** <https://github.com/chirag127/kirtuclub-downloader/releases>
> Downloaded content is never committed — the tool writes to a git-ignored `content/`.

`kirtuclub` fetches page images, assembles them into per-episode PDFs, adds a
searchable OCR text layer, and merges episodes into a single file — all from one
command tree, no shell scripts to chain by hand.

## Install

```bash
pipx install git+https://github.com/chirag127/kirtuclub-downloader
# or, from a clone:
pip install -e .
```

OCR needs the system `tesseract` + `ghostscript` binaries (via [OCRmyPDF]):

```bash
# Debian/Ubuntu
sudo apt-get install -y tesseract-ocr ghostscript
# macOS
brew install tesseract ghostscript
```

## Usage

```bash
kirtuclub --help                       # all subcommands
kirtuclub download --episodes 1 57     # fetch page images for a range
kirtuclub topdf                        # images → per-episode PDFs
kirtuclub ocr                          # add searchable text layer
kirtuclub merge                        # combine episodes into one PDF
kirtuclub pipeline --episodes 1 57     # run all four end to end
```

Every subcommand takes `--series`, `--content-dir`, and related flags; run
`kirtuclub <cmd> --help` for details.

### Configuration

All settings have sane defaults and can be overridden by CLI flags or `KIRTU_`
environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `KIRTU_SERIES` | `savita-bhabhi` | Series slug |
| `KIRTU_BASE_URL` | KirtuClub uploads path | Image base URL |
| `KIRTU_CONTENT_DIR` | `content` | Output directory (git-ignored) |
| `KIRTU_CONCURRENCY` | `8` | Parallel download workers |
| `KIRTU_MAX_PAGES` | `100` | Max pages probed per episode |
| `KIRTU_OCR_LANG` | `eng` | Tesseract language |
| `KIRTU_TEXT_THRESHOLD` | `50` | Chars/page below which OCR runs |
| `KIRTU_MAX_MERGE_MB` | `90` | Skip merged files over this size |

## Development

```bash
pip install -e ".[dev]" pillow
ruff check .
pytest -q
```

## How it works

```
download  →  topdf      →  ocr           →  merge
(images)     (img → PDF)   (ocrmypdf)       (per-episode → all-in-one)
```

The pipeline stages live in `src/kirtuclub_downloader/pipeline.py` and are pure
functions the CLI and tests drive identically.

## License

[MIT](LICENSE)

[OCRmyPDF]: https://github.com/ocrmypdf/OCRmyPDF
