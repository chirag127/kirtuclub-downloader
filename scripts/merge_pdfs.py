import argparse
import glob
import os
import PyPDF2


def merge_pdfs(pdfs, out_path):
    if os.path.exists(out_path):
        return
    merger = PyPDF2.PdfMerger()
    for pdf in sorted(pdfs):
        try:
            merger.append(pdf)
        except Exception:
            pass
    merger.write(out_path)
    if os.path.exists(out_path):
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        if size_mb > 90:
            os.remove(out_path)
            with open(os.path.join(os.path.dirname(out_path), "large.txt"), "w") as f:
                f.write(f"{out_path} was {size_mb:.0f} MB — too large to keep\n")


def collect_ocr_pdfs(search_root):
    return glob.glob(os.path.join(search_root, "**", "*_ocr.pdf"), recursive=True)


def main():
    parser = argparse.ArgumentParser(description="Merge OCR PDFs into single files")
    parser.add_argument("--root", default="content", help="Root directory to search for PDFs")
    args = parser.parse_args()

    folders = set()
    for pdf in collect_ocr_pdfs(args.root):
        folders.add(os.path.dirname(pdf))

    for folder in sorted(folders):
        pdfs = sorted(glob.glob(os.path.join(folder, "*_ocr.pdf")))
        out_name = folder.replace(os.sep, "_") + "_all_in_one.pdf"
        out_path = os.path.join(folder, out_name)
        merge_pdfs(pdfs, out_path)


if __name__ == "__main__":
    main()
