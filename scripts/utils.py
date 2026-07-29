import requests


def download_jpg(url, file_name):
    try:
        r = requests.get(url, timeout=10)
        if not r.ok:
            return False
        with open(file_name, "wb") as f:
            f.write(r.content)
        return True
    except Exception:
        return False
