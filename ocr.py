import os
import subprocess
from time import sleep
import traceback
import sys
from PyPDF2 import PdfReader


# ocrmypdf                      # it's a scriptable command line program
#    -l eng+fra                 # it supports multiple languages
#    --rotate-pages             # it can fix pages that are misrotated
#    --deskew                   # it can deskew crooked PDFs!
#    --title "My PDF"           # it can change output metadata
#    --jobs 4                   # it uses multiple cores by default
#    --output-type pdfa         # it produces PDF/A by default
#    input_scanned.pdf          # takes PDF input (or images)
#    output_searchable.pdf      # produces validated PDF output


def main(path="quantums/Big_Data_Quantum-m.pdf", nn=50):
    # import the required modules

    print(path)

    subprocess.call(
        [
            "git","pull"
        ]
    )

    if "_ocr" in path or "all_in_one" in path:
        return

    # ocr_file_name = "quantums/Big_Data_Quantum-m_ocr.pdf"
    ocr_file_name = path.replace(".pdf", "_ocr.pdf")

    # print("ocr_file_name", ocr_file_name)

    # define the path to the folder

    if os.path.exists(ocr_file_name):
        print("file already exist")
        return

    # creating a pdf reader object
    reader = PdfReader(path)

    # printing number of pages in pdf file
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
    text = all_text

    length = len(text)

    print("length", length)

    length_per_page = length / total_pages

    print("length_per_page", length_per_page)

    if length / total_pages < nn:
        print(
            f"""file need to be scanned with details
filepath : {path}
total_pages : {total_pages}
total_text_length : {length}
length_per_page : {length_per_page}
"""
        )

        subprocess.call(
            [
                "ocrmypdf",
                "-l",
                "eng",
                "--rotate-pages",
                "--deskew",
                "--force-ocr",
                path,
                ocr_file_name,
            ]
        )

        # commit and push ocr

        subprocess.call(["git", "add", "-A"])

        subprocess.call(["git", "commit", "-m", f"added {ocr_file_name}"])

        subprocess.call(["git", "push"])

    else:
        print("file is already scanned")

    # ocr_file_name = "quantums/Big_Data_Quantum-m_ocr.pdf"


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

    files = glob.glob("**/*.pdf", recursive=True)

    sorted(files)
    sorted_files = sorted(files)

    files = sorted_files

    # import random

    # random.shuffle(files)

    # from concurrent.futures import ProcessPoolExecutor

    # with ProcessPoolExecutor() as executor:
    #     executor.map(try_main, files)

    for i in files:
        try_main(i,200)