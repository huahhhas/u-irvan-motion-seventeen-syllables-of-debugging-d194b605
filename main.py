#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — make.fun bounty entry.

Writes exactly one haiku about debugging (3 lines, 5-7-5 syllables,
at most 200 characters, no trailing newline) to entry.txt.

Haiku (syllables counted by hand):
  "The breakpoint waits still"
    The(1) break-point(2) waits(1) still(1) = 5
  "a log line scrolls past midnight"
    a(1) log(1) line(1) scrolls(1) past(1) mid-night(2) = 7
  "and the bug was me"
    and(1) the(1) bug(1) was(1) me(1) = 5

Output: by default entry.txt next to this script; set OUTPUT_DIR to
write to <OUTPUT_DIR>/entry.txt instead (e.g. the workspace output dir).
Pure Python 3 standard library, no network, deterministic.
"""

import hashlib
import os

HAIKU = (
    "The breakpoint waits still\n"
    "a log line scrolls past midnight\n"
    "and the bug was me"
)

# Syllable count for every word in the haiku, counted by hand.
SYLLABLES = {
    "the": 1,
    "breakpoint": 2,
    "waits": 1,
    "still": 1,
    "a": 1,
    "log": 1,
    "line": 1,
    "scrolls": 1,
    "past": 1,
    "midnight": 2,
    "and": 1,
    "bug": 1,
    "was": 1,
    "me": 1,
}

EXPECTED = (5, 7, 5)


def count_syllables(line):
    total = 0
    for word in line.split():
        word = word.strip(".,;:!?\"'").lower()
        assert word in SYLLABLES, f"uncounted word: {word!r}"
        total += SYLLABLES[word]
    return total


def main():
    out_dir = os.environ.get("OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
    else:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    data = HAIKU.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Re-read and verify the gate: UTF-8, 3 lines, 5-7-5 syllables,
    # 1-200 chars, no trailing newline, exactly the intended haiku.
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    assert 1 <= len(text) <= 200, f"length {len(text)} out of range"
    assert not text.endswith("\n"), "entry must have no trailing newline"
    lines = text.split("\n")
    assert len(lines) == 3, f"expected 3 lines, got {len(lines)}"
    counts = tuple(count_syllables(line) for line in lines)
    assert counts == EXPECTED, f"syllable counts {counts} != {EXPECTED}"
    assert text == HAIKU, "entry does not match the intended haiku"
    assert raw == data, "file bytes differ from the intended encoding"
    print("sha256:", hashlib.sha256(raw).hexdigest())
    print("chars:", len(text), "bytes:", len(raw))
    print("syllables per line:", counts)


if __name__ == "__main__":
    main()
