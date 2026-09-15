#!/usr/bin/env python3
"""
Merges PDFs from a directory into a single PDF.
Example of usage: python3 merge_pdfs.py --path ~/data/pages/ --out Merged.pdf
"""

from pypdf import PdfReader, PdfWriter
import os
import re
import time
import argparse

PDF_PATH = "~/data/"
OUT_FILENAME = "Merged.pdf"


def natural_key(name):
    return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", name)]


def get_pdfs(path):
    items = os.listdir(path)
    items = [path + i for i in sorted(items, key=natural_key)]
    items = [i for i in items if os.path.isfile(i) and i.endswith(".pdf")]
    print("Found pdfs:", items, "\n")
    return items


def merge(pdf_paths, out_filename=OUT_FILENAME):
    if not pdf_paths:
        print("No PDFs found.")
        return
    writer = PdfWriter()
    t1 = time.perf_counter()
    print("Merging...")
    for pdf_path in pdf_paths:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
    t2 = time.perf_counter()
    print("... Took:", t2 - t1)
    out = os.path.split(pdf_paths[0])[0] + "/" + out_filename
    print("Saving...", out)
    with open(out, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge set of PDFs into single PDF")
    parser.add_argument("--path", help="path to PDFs to be merged, default: ~/data/")
    parser.add_argument("--out", help="output filename, default: Merged.pdf")
    args = parser.parse_args()
    path_to_pdfs = args.path and args.path or PDF_PATH
    path_to_pdfs = os.path.expanduser(path_to_pdfs)
    if not path_to_pdfs.endswith("/"):
        path_to_pdfs += "/"
    out_filename = args.out and args.out or OUT_FILENAME
    items = get_pdfs(path_to_pdfs)
    merge(items, out_filename)
