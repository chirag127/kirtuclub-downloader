"""HTTP layer — a small resilient client for fetching comic page images.

Wraps ``httpx`` with retry/backoff and a shared user-agent. Returns raw
bytes; callers decide where to write them.
"""

from __future__ import annotations

import time

import httpx

from .config import Config


class Downloader:
    """Fetch page images over HTTP with bounded retries."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = httpx.Client(
            headers={"User-Agent": config.user_agent},
            timeout=config.timeout,
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Downloader":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def fetch(self, url: str, *, retries: int = 3) -> bytes | None:
        """Return response bytes, or ``None`` on 404 / permanent failure.

        A 404 means "no such page" — the natural end of an episode — so it
        returns ``None`` without raising. Transient errors are retried with
        exponential backoff.
        """
        last_exc: Exception | None = None
        for attempt in range(1, retries + 1):
            try:
                resp = self._client.get(url)
                if resp.status_code == 404:
                    return None
                resp.raise_for_status()
                return resp.content
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return None
                last_exc = exc
            except httpx.HTTPError as exc:
                last_exc = exc
            if attempt < retries:
                time.sleep(0.5 * 2 ** (attempt - 1))
        if last_exc is not None:
            raise last_exc
        return None
