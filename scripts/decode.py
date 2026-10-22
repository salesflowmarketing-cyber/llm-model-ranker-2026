"""Decode Next.js client-side flight payloads.

Every leaderboard covered by this repo is client-side rendered: the HTML shell
contains no <table> rows, but the Next.js RSC "flight" stream embeds the full
dataset as escaped JSON inside `self.__next_f.push([1, "<payload>"])` calls.

`payloads()` concatenates those chunks into one string; `grab()` locates a
named JSON array inside it by brace/bracket matching and returns parsed JSON.
"""
import re
import json
import gzip
import os


def read_text(path):
    """Read a text file, transparently handling .gz (and falling back to path + '.gz')."""
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        path = path + ".gz"
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def read_json(path):
    """Read and parse a JSON file, transparently handling .gz."""
    return json.loads(read_text(path))


def payloads(path):
    """Return the concatenated RSC flight payload for a cached HTML/JSON page."""
    t = read_text(path)
    out = []
    for m in re.finditer(r'self\.__next_f\.push\(\[1,\s*(".*?")\]\)</script>', t, flags=re.S):
        try:
            out.append(json.loads(m.group(1)))
        except Exception:
            pass
    if not out:
        # Fall back to any inline <script> that looks like JSON.
        for m in re.finditer(r'<script[^>]*>(.*?)</script>', t, flags=re.S):
            s = m.group(1).strip()
            if s.startswith("{") or s.startswith("["):
                out.append(s)
    return "".join(out), t


def grab(s, key, occ=0):
    """Extract and parse the JSON array stored under `key` in a flight payload."""
    idxs = [m.start() for m in re.finditer(r'"%s":\s*\[' % re.escape(key), s)]
    if not idxs:
        return None
    i = idxs[min(occ, len(idxs) - 1)]
    j = s.find("[", i)
    depth = 0
    k = j
    instr = False
    esc = False
    while k < len(s):
        c = s[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    break
        k += 1
    blob = s[j:k + 1]
    try:
        return json.loads(blob)
    except Exception:
        return None
