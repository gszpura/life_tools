#!/usr/bin/env bash
# Installs life_tools PDF scripts globally by symlinking them into ~/.local/bin
# and installing required Python dependencies.
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_DIR="${HOME}/.local/bin"
SCRIPTS=(
    src/pdfs/images_to_pdf.py
    src/pdfs/pdf_to_pages.py
    src/pdfs/merge_pdfs.py
    src/meta/toolist.py
)

echo "Installing dependencies from requirements.txt..."
python3 -m pip install -r "${REPO_DIR}/requirements.txt"

mkdir -p "${BIN_DIR}"
for rel in "${SCRIPTS[@]}"; do
    src="${REPO_DIR}/${rel}"
    if [ ! -f "${src}" ]; then
        echo "Missing script: ${src}" >&2
        exit 1
    fi
    chmod +x "${src}"
    ln -sf "${src}" "${BIN_DIR}/$(basename "${rel}" .py)"
    echo "Installed: $(basename "${rel}" .py) -> ${src}"
done

case ":${PATH}:" in
    *":${BIN_DIR}:"*) ;;
    *)
        echo "WARNING: ${BIN_DIR} is not on your PATH."
        echo 'Add this to your shell profile: export PATH="$HOME/.local/bin:$PATH"'
        ;;
esac

echo "Done. Try: images_to_pdf --help"
