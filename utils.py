
import requests


def download_jpg(url, file_name):

    try:

        r = requests.get(url,timeout=5)

        print("status_code", r.status_code)

        print("url", url)

        if r.ok is True:



            with open(file_name, "wb") as f:
                f.write(r.content)

            return True
        else:

            return False

    except Exception as e:

        print(e)

        return False