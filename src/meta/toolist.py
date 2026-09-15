#!/usr/bin/env python3
"""
Lists all life_tools with one-sentence descriptions, taken from each script's docstring.
Example of usage: python3 toolist.py
"""

import ast
import os

SRC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_scripts(src_dir):
    scripts = []
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not d.startswith((".", "__"))]
        for f in sorted(files):
            if f.endswith(".py") and f != "__init__.py":
                scripts.append(os.path.join(root, f))
    return sorted(scripts)


def get_description(path):
    with open(path) as f:
        tree = ast.parse(f.read(), filename=path)
    doc = ast.get_docstring(tree)
    if not doc:
        return "No description."
    return doc.strip().splitlines()[0].strip()


def main():
    scripts = get_scripts(SRC_DIR)
    if not scripts:
        print("No tools found.")
        return
    width = max(len(os.path.splitext(os.path.basename(s))[0]) for s in scripts)
    for path in scripts:
        name = os.path.splitext(os.path.basename(path))[0]
        print("{}  {}".format(name.ljust(width), get_description(path)))


if __name__ == "__main__":
    main()
