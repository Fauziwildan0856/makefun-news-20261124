#!/usr/bin/env python3
"""Entry program for the make.fun news-image bounty of 24 Nov 2026.

Beside this file sits a finished newspaper page, entry.png: "THE
WORLD IN ONE PAGE" for Tuesday 24 November 2026, holding fifty
stories from that one day on a single 1024x1024 sheet. The page
was drawn with code while this entry was being prepared; nothing
in this program draws. Its whole job is publication:

  1. find the stored page in this folder, whatever name the
     upload left it with;
  2. prove the found file is the entered page, by its SHA-256
     fingerprint and by the limits the bounty sets on a PNG;
  3. copy those exact bytes to entry.png inside the output
     directory, then read the copy back and prove it again.

Only the Python standard library is touched, because the grading
machine is a bare Python with no network and no extra packages.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

# The entered page, identified by its fingerprint. Any file whose
# bytes hash to something else is not the page, whatever its name.
EXPECTED_SHA256 = "65bcd64f46367770da291afac4f3d1ad7f2cab4b18489ab4a7979f392037682e"

# The name the rules suggest comes first; the others are names
# that phone uploads have produced before and may produce again.
ENTRY_NAMES = [
    "entry.png",
    "image (2).png",
    "image (1).png",
    "image.png",
    "entry (1).png",
    "image (3).png",
    "entry (3).png",
]

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SIDE_LIMIT = 1024        # the bounty caps the picture at 1024x1024
BYTE_LIMIT = 1048576     # ... and at one mebibyte


def sha256_of(path):
    """Hex SHA-256 of a file, streamed in blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def png_size(data):
    """(width, height) declared by a PNG's IHDR header.

    Only the first 24 bytes matter: the 8-byte signature, then the
    IHDR chunk's length and type, then width and height as big
    endian words. The image data is never decoded here.
    """
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("PNG header is missing its IHDR chunk")
    return struct.unpack(">II", data[16:24])


def find_entry(folder):
    """Locate the entered page inside *folder*.

    Preferred names are tried first; each existing file is accepted
    only when its fingerprint matches, and a mismatch is reported
    before moving on, since a later name may still be the page. If
    no preferred name matches, every other PNG in the folder gets
    the same test, so a name nobody predicted cannot lose the
    entry while the right bytes sit beside the program.
    """
    tried = set()
    for name in ENTRY_NAMES:
        tried.add(name)
        path = folder / name
        if path.is_file():
            if sha256_of(path) == EXPECTED_SHA256:
                return path
            print("warning: %s exists but is not the entered page"
                  % name, file=sys.stderr)
    for path in sorted(folder.glob("*.png")):
        if path.name in tried or not path.is_file():
            continue
        if sha256_of(path) == EXPECTED_SHA256:
            print("note: the entered page is named %s here"
                  % path.name, file=sys.stderr)
            return path
    raise FileNotFoundError("no file in %s matches the entered "
                            "page's fingerprint" % folder)


def output_path():
    """Where the published page belongs.

    MAKEFUN_OUTPUT_DIR wins when the grader sets it; /output is
    the fallback the bounty describes; the program's own folder is
    the last resort so a plain local run still produces the file.
    """
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not chosen and os.path.isdir("/output"):
        chosen = "/output"
    if not chosen:
        chosen = str(Path(__file__).resolve().parent)
    return Path(chosen) / "entry.png"


def run():
    folder = Path(__file__).resolve().parent
    source = find_entry(folder)
    data = source.read_bytes()

    # Gate on the fingerprint first: after this line, `data` is
    # known to be the entered page and nothing else.
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise IOError("the bytes read are not the entered page")
    if len(data) > BYTE_LIMIT:
        raise ValueError("the page is %d bytes, over the 1 MiB "
                         "limit" % len(data))
    width, height = png_size(data)
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ValueError("the page is %dx%d, over the 1024x1024 "
                         "limit" % (width, height))

    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

    # A short write would otherwise surface only at judging time;
    # catch it here instead, while the failure is still ours.
    if sha256_of(target) != EXPECTED_SHA256:
        raise IOError("the published copy failed verification")

    print("published %s (%d bytes, %dx%d) to %s"
          % (source.name, len(data), width, height, target))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except (FileNotFoundError, ValueError, IOError, OSError) as exc:
        # Every failure above means "this entry cannot be
        # published", so say that plainly and exit non-zero rather
        # than dumping a traceback on the grader.
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(1)
