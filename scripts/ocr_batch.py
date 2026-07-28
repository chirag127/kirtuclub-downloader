import os
import subprocess
from time import sleep
import traceback
import sys
from PyPDF2 import PdfReader


def main(path="content/savita-bhabhi/episode-01-to-57/"):
    print(path)
    subprocess.call(["git", "pull"])
    if "_ocr" in path or "all_in_one" in path:
        return
    ocr_file_name = path.replace(".pdf", "_ocr.pdf")
    if os.path.exists(ocr_file_name):
        print("file already exist")
        return
    reader = PdfReader(path)
    print("total_pages", len(reader.pages))
    total_pages = len(reader.pages)
    all_text = ""
    if total_pages > 10:
        import random
        random_sample = random.sample(range(total_pages), 10)
        total_pages = 10
    else:
        random_sample = range(total_pages)
    for i in random_sample:
        page = reader.pages[i]
        try:
            text = page.extract_text()
            all_text += text
        except Exception as error:
            print("error", error)
    length = len(all_text)
    print("length", length)
    length_per_page = length / total_pages
    print("length_per_page", length_per_page)
    nn = 50
    if length / total_pages < nn:
        print("file need to be scanned with details")
        print("filepath :", path)
        print("total_pages :", total_pages)
        print("total_text_length :", length)
        print("length_per_page :", length_per_page)
        subprocess.call([
            "ocrmypdf", "-l", "eng",
            "--force-ocr",
            path, ocr_file_name,
        ])
        subprocess.call(["git", "add", "-A"])
        subprocess.call(["git", "commit", "-m", "added " + ocr_file_name])
        subprocess.call(["git", "push"])
    else:
        print("file is already scanned")


def try_main(i, nn=50):
    try:
        main(i, nn)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        sleep(10)


if __name__ == "__main__":
    import glob
    files = glob.glob("content/savita-bhabhi/episode-01-to-57/**/*.pdf", recursive=True)
    sorted_files = sorted(files)
    files = sorted_files[::-1]
    for i in files:
        try_main(i, 200)