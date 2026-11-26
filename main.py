#!/usr/bin/env python3
"""Write the entry line to $MAKEFUN_OUTPUT_DIR/entry.txt.

Pure Python standard library only. Validates the line against the
competition gate (one line, 120 characters at most, non-blank,
valid UTF-8) before writing, and exits non-zero on any failure.
"""

import os
import sys

LINE = '★☆☆☆☆ Controls the tides, never pays rent, vanishes for days every month with no explanation. Worst roommate ever.'
MAX_CHARS = 120


def main() -> int:
    text = LINE
    if not text or not text.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            "error: entry is %d characters, over the %d limit" % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print("error: entry is not valid UTF-8: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    old_umask = os.umask(0o022)
    try:
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.chmod(path, 0o644)
    finally:
        os.umask(old_umask)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
