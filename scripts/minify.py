#!/usr/bin/env python3
"""Minify CSS and JS for production."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", text)
    return text.strip()


def minify_js(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(?m)^\s*//.*$", "", text)
    text = re.sub(r"\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main():
    css_src = ROOT / "css" / "style.css"
    fonts = (ROOT / "css" / "fonts.css").read_text(encoding="utf-8")
    css = fonts + "\n" + css_src.read_text(encoding="utf-8")
    (ROOT / "css" / "style.min.css").write_text(minify_css(css), encoding="utf-8")
    print("Built css/style.min.css")

    js = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
    (ROOT / "js" / "main.min.js").write_text(minify_js(js), encoding="utf-8")
    print("Built js/main.min.js")


if __name__ == "__main__":
    main()
