"""Tests for the pipeline stages — no network, no external OCR binary."""

from __future__ import annotations

import os

import img2pdf
import pytest
from PIL import Image

from kirtuclub_downloader import pipeline
from kirtuclub_downloader.config import Config


def _make_jpg(path: str, size: tuple[int, int] = (32, 32)) -> None:
    Image.new("RGB", size, (200, 120, 60)).save(path, "JPEG")


@pytest.fixture()
def cfg(tmp_path) -> Config:
    base = Config()
    return Config(**{**base.__dict__, "content_dir": str(tmp_path)})


def test_images_to_pdf_builds_file(tmp_path):
    imgs = []
    for i in range(1, 4):
        p = tmp_path / f"{i:03d}.jpg"
        _make_jpg(str(p))
        imgs.append(str(p))
    out = str(tmp_path / "ep.pdf")
    assert pipeline.images_to_pdf(imgs, out) is True
    assert os.path.exists(out)
    assert os.path.getsize(out) > 0


def test_images_to_pdf_empty_returns_false(tmp_path):
    assert pipeline.images_to_pdf([], str(tmp_path / "x.pdf")) is False


def test_images_to_pdf_skips_existing(tmp_path):
    p = tmp_path / "a.jpg"
    _make_jpg(str(p))
    out = tmp_path / "ep.pdf"
    out.write_bytes(b"%PDF-existing")
    assert pipeline.images_to_pdf([str(p)], str(out)) is True
    assert out.read_bytes() == b"%PDF-existing"  # untouched


def test_merge_pdfs_combines(tmp_path, cfg):
    pdfs = []
    for i in range(2):
        img = tmp_path / f"{i}.jpg"
        _make_jpg(str(img))
        pdf = tmp_path / f"{i}.pdf"
        pdf.write_bytes(img2pdf.convert([str(img)]))
        pdfs.append(str(pdf))
    out = str(tmp_path / "all_in_one.pdf")
    assert pipeline.merge_pdfs(pdfs, out, cfg) is True
    assert os.path.exists(out)


def test_merge_pdfs_over_cap_removed(tmp_path):
    img = tmp_path / "a.jpg"
    _make_jpg(str(img))
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(img2pdf.convert([str(img)]))
    tiny_cap = Config(**{**Config().__dict__, "max_merge_mb": 0})
    out = str(tmp_path / "big.pdf")
    assert pipeline.merge_pdfs([str(pdf)], out, tiny_cap) is False
    assert not os.path.exists(out)


def test_needs_ocr_on_image_pdf_true(tmp_path, cfg):
    img = tmp_path / "a.jpg"
    _make_jpg(str(img))
    pdf = str(tmp_path / "scan.pdf")
    with open(pdf, "wb") as fh:
        fh.write(img2pdf.convert([str(img)]))
    assert pipeline.needs_ocr(pdf, cfg) is True


def test_needs_ocr_skips_ocr_named(tmp_path, cfg):
    p = str(tmp_path / "scan_ocr.pdf")
    open(p, "wb").close()
    assert pipeline.needs_ocr(p, cfg) is False


def test_find_pdfs_recursive(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "x.pdf").write_bytes(b"%PDF")
    (tmp_path / "y.pdf").write_bytes(b"%PDF")
    found = pipeline.find_pdfs(str(tmp_path))
    assert len(found) == 2


class _FakeDownloader:
    """Serves 3 pages then 404 (None)."""

    def __init__(self, pages: int = 3):
        self._pages = pages

    def fetch(self, url: str, retries: int = 3):  # noqa: ARG002
        # url ends with -<page>.jpg
        page = int(url.rsplit("-", 1)[-1].split(".")[0])
        return b"\xff\xd8\xff" if page <= self._pages else None


def test_download_episode_stops_at_404(cfg):
    saved = pipeline.download_episode(_FakeDownloader(3), cfg, episode=1)
    assert len(saved) == 3
    assert all(os.path.exists(p) for p in saved)
