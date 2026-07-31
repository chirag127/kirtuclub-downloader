"""Runtime configuration, resolved from CLI flags then environment.

Every value has a sane default so the tool runs with zero configuration.
Environment variables use the ``KIRTU_`` prefix.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://kirtuclub.com/wp-content/uploads/2023/05"
DEFAULT_SERIES = "savita-bhabhi"
DEFAULT_CONTENT_DIR = "content"
DEFAULT_TIMEOUT = 15.0
DEFAULT_CONCURRENCY = 8
DEFAULT_MAX_PAGES = 100
DEFAULT_OCR_LANG = "eng"
DEFAULT_TEXT_THRESHOLD = 50
DEFAULT_MAX_MERGE_MB = 90


def _env(name: str, default: str) -> str:
    return os.environ.get(f"KIRTU_{name}", default)


@dataclass(frozen=True)
class Config:
    """Resolved settings for a single CLI invocation."""

    base_url: str = _env("BASE_URL", DEFAULT_BASE_URL)
    series: str = _env("SERIES", DEFAULT_SERIES)
    content_dir: str = _env("CONTENT_DIR", DEFAULT_CONTENT_DIR)
    timeout: float = float(_env("TIMEOUT", str(DEFAULT_TIMEOUT)))
    concurrency: int = int(_env("CONCURRENCY", str(DEFAULT_CONCURRENCY)))
    max_pages: int = int(_env("MAX_PAGES", str(DEFAULT_MAX_PAGES)))
    ocr_lang: str = _env("OCR_LANG", DEFAULT_OCR_LANG)
    text_threshold: int = int(_env("TEXT_THRESHOLD", str(DEFAULT_TEXT_THRESHOLD)))
    max_merge_mb: int = int(_env("MAX_MERGE_MB", str(DEFAULT_MAX_MERGE_MB)))
    user_agent: str = _env(
        "USER_AGENT",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    )
