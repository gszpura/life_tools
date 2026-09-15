#!/usr/bin/env python3
"""
Dissolves a PDF into separate one-page PDFs.
Example of usage: python3 pdf_to_pages.py --path ~/data/doc.pdf --out ~/data/pages/
"""

from pypdf import PdfReader, PdfWriter
import os
import time
import argparse

PDF_PATH = "~/data/"
OUT_DIR = ""


def get_pdfs(path):
    if os.path.isdir(path):
        items = os.listdir(path)
        items = [path + i for i in sorted(items)]
        items = [i for i in items if os.path.isfile(i) and i.endswith(".pdf")]
    else:
        if not path.endswith(".pdf"):
            raise ValueError("Not a PDF file: " + path)
        items = [path]
    print("Found pdfs:", items, "\n")
    return items


def dissolve(pdf_path, out_dir):
    reader = PdfReader(pdf_path)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    t1 = time.perf_counter()
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(out_dir, "{}_page_{}.pdf".format(base, i + 1))
        with open(out, "wb") as f:
            writer.write(f)
        print("Saved:", out)
    t2 = time.perf_counter()
    print("... Took:", t2 - t1)


def main():
    parser = argparse.ArgumentParser(
        description="Dissolve PDFs into separate one-page PDFs"
    )
    parser.add_argument(
        "--path", help="path to a PDF file or a directory with PDFs, default: ~/data/"
    )
    parser.add_argument("--out", help="output directory, default: <pdf dir>/pages/")
    args = parser.parse_args()
    path = args.path and args.path or PDF_PATH
    path = os.path.expanduser(path)
    pdfs = get_pdfs(path)
    if not pdfs:
        print("No PDFs found.")
        return
    out_dir = args.out and os.path.expanduser(args.out) or OUT_DIR
    if not out_dir:
        out_dir = os.path.join(os.path.split(pdfs[0])[0], "pages")
    os.makedirs(out_dir, exist_ok=True)
    for pdf in pdfs:
        dissolve(pdf, out_dir)


if __name__ == "__main__":
    main()
