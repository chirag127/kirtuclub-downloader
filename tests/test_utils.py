import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from unittest.mock import patch, MagicMock
import tempfile


def test_download_jpg_success():
    sys.modules["requests"] = MagicMock()
    requests_mock = sys.modules["requests"]
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.content = b"fake_image_data"
    mock_response.status_code = 200
    requests_mock.get.return_value = mock_response

    from utils import download_jpg

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        tmp_path = f.name

    result = download_jpg("https://example.com/img.jpg", tmp_path)
    assert result is True
    with open(tmp_path, "rb") as f:
        assert f.read() == b"fake_image_data"
    os.unlink(tmp_path)


def test_download_jpg_failure():
    sys.modules["requests"] = MagicMock()
    requests_mock = sys.modules["requests"]
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    requests_mock.get.return_value = mock_response

    from utils import download_jpg

    result = download_jpg("https://example.com/img.jpg", "/nonexistent/test.jpg")
    assert result is False


def test_download_jpg_exception():
    sys.modules["requests"] = MagicMock()
    requests_mock = sys.modules["requests"]
    requests_mock.get.side_effect = Exception("connection error")

    from utils import download_jpg

    result = download_jpg("https://example.com/img.jpg", "/nonexistent/test.jpg")
    assert result is False
