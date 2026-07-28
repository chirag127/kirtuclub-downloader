import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from unittest.mock import patch, MagicMock
import tempfile


def test_merge_pdfs_skips_when_output_exists():
    sys.modules["PyPDF2"] = MagicMock()

    from merge_pdfs import merge_pdfs

    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = os.path.join(tmpdir, "out.pdf")
        with open(out_path, "w") as f:
            f.write("existing")
        result = merge_pdfs(tmpdir, out_path)
        assert result is None


def test_merge_pdfs_skips_when_large_txt_exists():
    sys.modules["PyPDF2"] = MagicMock()

    from merge_pdfs import merge_pdfs

    with tempfile.TemporaryDirectory() as tmpdir:
        large_txt = os.path.join(tmpdir, "large.txt")
        with open(large_txt, "w") as f:
            f.write("skip")
        out_path = os.path.join(tmpdir, "merged.pdf")
        result = merge_pdfs(tmpdir, out_path)
        assert result is None


def test_merge_pdfs_calls_merger():
    sys.modules["PyPDF2"] = MagicMock()

    from merge_pdfs import merge_pdfs

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test_ocr.pdf")
        with open(pdf_path, "w") as f:
            f.write("%PDF-1.4 mock")
        out_path = os.path.join(tmpdir, "merged.pdf")

        with patch("merge_pdfs.PyPDF2.PdfMerger") as mock_merger_class:
            mock_merger = MagicMock()
            mock_merger_class.return_value = mock_merger
            with patch("merge_pdfs.glob.glob", return_value=[pdf_path]):
                with patch("os.path.getsize", return_value=1000):
                    merge_pdfs(tmpdir, out_path)
                    mock_merger.append.assert_called_once_with(pdf_path)
                    mock_merger.write.assert_called_once()
