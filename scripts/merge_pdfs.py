"""Merge all PDFs in subdirectories into single PDF files."""
import glob
import os
import PyPDF2


def merge_pdfs(parent_dir, out_full_path):
    if not os.path.exists(out_full_path):
        if os.path.exists(os.path.join(parent_dir, "large.txt")):
            print("large.txt exists, so we will not merge the pdfs")
            return
        pdfs = glob.glob(os.path.join(parent_dir, "/**/*_ocr.pdf"), recursive=True)
        pdfs.sort()
        print(pdfs)
        merger = PyPDF2.PdfMerger()
        for pdf in pdfs:
            try:
                if os.path.getsize(out_full_path) > 50000000 or "_in_one.pdf" in pdf:
                    print("output file is too large, so we will not merge the pdfs")
                    continue
                merger.append(pdf)
            except Exception as error:
                print(error)
                print("error with", pdf)
        merger.write(out_full_path)
        if os.path.getsize(out_full_path) > 90000000:
            os.remove(out_full_path)
            print("deleted", out_full_path)
            with open(os.path.join(parent_dir, "large.txt"), "w") as file:
                file.write("The following files are too large to be merged into one pdf file: \n")
                for pdf in pdfs:
                    file.write(pdf + " is of size " + str(os.path.getsize(pdf)) + "\n")
        else:
            print("kept", out_full_path)


def main():
    all_pdfs = glob.glob("**/*.pdf", recursive=True)
    folders = []
    for pdf_file in all_pdfs:
        parent_dir = os.path.dirname(pdf_file)
        folders.append(parent_dir)
    folders = list(set(folders))
    print(folders)
    for parent_dir in folders:
        print(parent_dir)
        out_full_path = os.path.join(parent_dir, parent_dir.replace("/", "_") + "_all_in_one.pdf")
        try:
            merge_pdfs(parent_dir, out_full_path)
        except Exception as error:
            print(error)
            print("error with", parent_dir)


if __name__ == "__main__":
    main()