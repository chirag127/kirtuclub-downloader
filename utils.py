
import requests


def download_jpg(url, file_name):

    r = requests.get(url)

    if r.ok is True:



        with open(file_name, "wb") as f:
            f.write(r.content)

        return True
    else:

        return False