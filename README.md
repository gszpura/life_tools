Various tools
============

## Installation
```bash
git clone git@github.com:gszpura/life_tools.git
cd life_tools
scripts/install.sh
```

The installer installs Python dependencies from `requirements.txt` and symlinks the PDF and meta tools into **~/.local/bin**, making them available globally:

-- **images_to_pdf** — convert images to a single PDF
-- **pdf_to_pages** — dissolve a PDF into one-page PDFs
-- **merge_pdfs** — merge PDFs into a single PDF
-- **toolist** — list all tools with short descriptions

Logo tools are not installed globally; run them from the repo root (see **logos/README.md**).

## Tools
* Tool for listing all tools with short descriptions
  
-- example usage: **python3** src/meta/toolist.py (or globally: **toolist**, after running scripts/install.sh)

## PDF Tools
* Tool for converting multiple images to PDF
  
-- example usage: **python3** images_to_pdf.py --path ~/data/ --resize 0.5 --rotate 90

* Tool for dissolving a PDF into separate one-page PDFs

-- example usage: **python3** pdf_to_pages.py --path ~/data/doc.pdf --out ~/data/pages/

-- `--path` can be a single PDF file or a directory with PDFs; output goes to `--out` directory (default: `<pdf dir>/pages/`), pages saved as `<name>_page_N.pdf`

* Tool for merging multiple PDFs into a single PDF

-- example usage: **python3** merge_pdfs.py --path ~/data/pages/ --out Merged.pdf

-- `--path` is a directory with PDFs; pages are merged in natural order (page_2 before page_10), output saved as `--out` (default: `Merged.pdf`) in the input directory

## Logo Tools
See **logos/README.md** for logo generation, text, rotation and color conversion tools.
