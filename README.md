Various tools
============

* Tool for converting multiple images to PDF
  
-- example usage: **python3** images_to_pdf.py --path ~/data/ --resize 0.5 --rotate 90

* Tool for dissolving a PDF into separate one-page PDFs

-- example usage: **python3** pdf_to_pages.py --path ~/data/doc.pdf --out ~/data/pages/

-- `--path` can be a single PDF file or a directory with PDFs; output goes to `--out` directory (default: `<pdf dir>/pages/`), pages saved as `<name>_page_N.pdf`

* Tool for merging multiple PDFs into a single PDF

-- example usage: **python3** merge_pdfs.py --path ~/data/pages/ --out Merged.pdf

-- `--path` is a directory with PDFs; pages are merged in natural order (page_2 before page_10), output saved as `--out` (default: `Merged.pdf`) in the input directory
