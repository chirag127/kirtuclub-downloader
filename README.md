# kirtuclub-downloader

> A Python CLI to download, assemble, OCR, and merge comic-page PDFs from KirtuClub — one pipeline: download to topdf to ocr to merge.

[![License](https://img.shields.io/github/license/chirag127/kirtuclub-downloader?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/chirag127/kirtuclub-downloader?style=flat-square)](https://github.com/chirag127/kirtuclub-downloader/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/chirag127/kirtuclub-downloader?style=flat-square)](https://github.com/chirag127/kirtuclub-downloader/commits)
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)](https://python.org)

**GHP landing** https://chirag127.github.io/kirtuclub-downloader/ · **Repo** https://github.com/chirag127/kirtuclub-downloader

⭐ If this is useful, please star the repo — it helps others find it.

`kirtuclub-downloader` is a single command-line tool (`kirtuclub`) that automates a four-step pipeline: download page images from KirtuClub, assemble them into per-episode PDFs, add a searchable OCR text layer, and merge the results into one file. It targets adult-content material published on KirtuClub; this repository contains only code — no media is included or distributed.

> Downloaded images and PDFs are not stored in the repo. The content directory the tool creates is git-ignored (along with `*.pdf`, `*.jpg`, `*.zip`, `*.cbz`, `*.cbr`). Run the tool to fetch your own.

## Pipeline

```mermaid
flowchart LR
    A[download] -->|page .jpg per episode| B[content/&lt;series&gt;/images]
    B --> C[topdf]
    C -->|per-episode .pdf| D[ocr]
    D -->|ocrmypdf adds text layer| E[searchable PDFs]
    E --> F[merge]
    F -->|combine per folder| G[all_in_one.pdf]
```

## Features

- **`download`** — fetches page images for a series/episode range from a configurable base URL into per-episode directories, skipping files that already exist.
- **`topdf`** — assembles the downloaded images into per-episode PDFs.
- **`ocr`** — detects text-less PDFs and runs `ocrmypdf` to add a searchable text layer (skips ones that already have text unless `--force`).
- **`merge`** — combines per-episode PDFs into a single `all_in_one.pdf`, respecting a size cap.
- **`pipeline`** — runs all four stages end to end (`--skip-ocr` to skip OCR).
- Rich terminal progress via [`rich`](https://github.com/Textualize/rich); CLI built with [`click`](https://click.palletsprojects.com).

## Tech stack

- **Python 3.10+**, packaged with a `pyproject.toml` (installable, exposes the `kirtuclub` entry point)
- `click` (CLI), `rich` (progress/output), `requests` (HTTP), PDF assembly/merge libs
- `ocrmypdf` invoked as a subprocess for the OCR step — its system dependencies (Tesseract, Ghostscript) must be installed separately
- Tests with `pytest`; linting with `ruff`

## Repo structure

```
kirtuclub-downloader/
├── pyproject.toml                     # package metadata + `kirtuclub` entry point
├── src/kirtuclub_downloader/
│   ├── cli.py                         # click CLI: download/topdf/ocr/merge/pipeline
│   ├── pipeline.py                    # the pipeline steps (download, images_to_pdf, ocr, merge)
│   ├── http.py                        # HTTP Downloader (session, retries)
│   └── config.py                      # Config defaults (series, base URL, dirs)
└── tests/
    └── test_pipeline.py               # pipeline tests
```

The content directory (created at runtime) and all downloaded media are git-ignored.

## Quick start

```bash
git clone https://github.com/chirag127/kirtuclub-downloader && cd kirtuclub-downloader
pip install -e .
# also install ocrmypdf's system deps (Tesseract, Ghostscript) for the OCR step
kirtuclub --help
```

## Usage

```bash
# run the whole pipeline for an episode range
kirtuclub pipeline --series <slug> --episodes 1 57

# or run stages individually
kirtuclub download --series <slug> --episodes 1 57
kirtuclub topdf    --series <slug>
kirtuclub ocr                       # add OCR text layer
kirtuclub merge                     # combine into all_in_one.pdf
```

Every subcommand supports `-h/--help` for its full argument list.

## Configuration

Configuration is via command-line flags (with sensible defaults in `config.py`), not environment variables:

| Flag | Command | Purpose |
|---|---|---|
| `--series` | download / topdf / merge | series slug |
| `--episodes START END` | download / pipeline | inclusive episode range |
| `--content-dir` | all | base output directory |
| `--base-url` | download | image base URL |
| `--root` | ocr / merge | directory to scan |
| `--force` | ocr | OCR even if text is detected |
| `--out` | merge | merged output path |
| `--skip-ocr` | pipeline | skip the OCR stage |

## Part of the oriz family

One of ~80 sites and tools in the oriz family. See [blog.oriz.in](https://blog.oriz.in).

## Contributing

Issues and PRs welcome. Keep changes minimal and never commit any downloaded media.

## Status

Maintained as a personal utility.

## License

MIT © Chirag Singhal — chirag@oriz.in

Conventional commits are the changelog.
