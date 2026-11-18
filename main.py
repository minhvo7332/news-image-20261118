#!/usr/bin/env python3
"""news-image-20261118 entry: deliver the finished front page.

The image (entry.png, 1024x1024) was drawn by draw_image.py from
reporting on Wednesday 18 November 2026 and is baked into this
repository. This program only copies those bytes to the output
directory, so the two grader runs write byte-identical files.
Python 3.13 standard library only; no network, no randomness.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly the bytes in the file: never ship a
    # truncated copy, so fail loudly if the sizes disagree.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy incomplete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
