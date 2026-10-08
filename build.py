"""Build the GitHub Pages version of the site.

index.html is written for the Claude artifact viewer, which wraps it in its own
document skeleton. GitHub Pages serves files as-is, so this script wraps the
same content in a complete HTML document and copies the images into docs/.

Run:  python build.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"

src = (ROOT / "index.html").read_text(encoding="utf-8")

# Lift the charset meta and <title> out of the body into the head.
src = src.replace('<meta charset="utf-8">\n', "", 1)
m = re.search(r"<title>(.*?)</title>\n", src)
title = m.group(1) if m else "DMV Weekly Book Club"
src = src.replace(m.group(0), "", 1) if m else src

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="A weekly online book club hosted by Danni: what we have read, what we are reading, book suggestions, finance picks and how to join.">
<style>
  html {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
  [hidden] {{ display: none !important; }}
  img {{ max-width: 100%; }}
</style>
</head>
<body>
"""
tail = "\n</body>\n</html>\n"

OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(head + src.strip("\n") + tail, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
for folder in ("covers", "photos"):
    dest = OUT / folder
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(ROOT / folder, dest)

print(f"built {OUT / 'index.html'} ({(OUT / 'index.html').stat().st_size:,} bytes)")
