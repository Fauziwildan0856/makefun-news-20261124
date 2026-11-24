#!/usr/bin/env python3
"""Publish the entered front page for make.fun's news-image bounty
of Tuesday 24 November 2026.

The page itself — "THE WORLD IN ONE PAGE", a 1024x1024 newspaper
front page holding 50 stories from 24 November 2026 — is finished
artwork kept beside this file as entry.png. It was drawn in code
while the entry was built: ocean-blue paper, thick yellow frames,
purple story text, a red date check, and a world map whose
continents carry their own colours. This program does not draw
anything: it finds that stored picture, proves it is the picture
that was entered, and publishes it unchanged as entry.png in the
output directory the bounty names.

Two proofs run before anything is published. First, the picture's
SHA-256 fingerprint must match the value recorded below; any other
bytes stop the program instead of publishing the wrong picture.
Second, the picture's PNG header must say it is a PNG no larger
than 1024 by 1024, the size the bounty allows.

The stored picture may carry any of the names in CANDIDATE_NAMES:
a phone upload does not always keep the name a file was given.
The fingerprint makes the choice safe — a wrong file cannot
match it, whatever it is called.

Nothing beyond the Python standard library is used, so the
program runs in the bare grading environment: no network, no
installed packages, no Pillow.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

# Fingerprint of the entered picture, "THE WORLD IN ONE PAGE —
# Tuesday, November 24, 2026": 50 stories on one 1024x1024 page.
PICTURE_SHA256 = (
    "65bcd64f46367770da291afac4f3d1ad7f2cab4b18489ab4a7979f392037682e"
)

# Names the picture may carry in this repository, tried in order.
# The first is the name the bounty rules suggest; the rest are
# names a phone upload has actually produced in the past.
CANDIDATE_NAMES = (
    "entry.png",
    "image (2).png",
    "image (1).png",
    "image.png",
    "entry (1).png",
)

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_SIDE = 1024
MAX_BYTES = 1024 * 1024


def fingerprint(path):
    """Return the SHA-256 hex digest of the file at *path*."""
    with open(path, "rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def picture_dimensions(data):
    """Return the (width, height) a PNG's header declares.

    The size lives in the IHDR chunk, right after the 8-byte PNG
    signature and the chunk's length and type fields. Reading the
    header is enough; the picture itself is never decoded.
    """
    if data[:8] != PNG_MAGIC:
        raise ValueError("the entered picture is not a PNG file")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("the entered picture has no PNG header")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def locate_picture(directory):
    """Return the path of the entered picture inside *directory*.

    Each candidate name is tried in turn. The first file that
    exists and matches the recorded fingerprint wins; a file that
    exists but fails the fingerprint is skipped with a warning,
    because the next name may still be the right picture. When no
    candidate matches, any other PNG in the folder is tried the
    same way, so an upload name nobody foresaw does not sink the
    entry while the right bytes are sitting right there.
    """
    folder = Path(directory)
    for name in CANDIDATE_NAMES:
        candidate = folder / name
        if not candidate.is_file():
            continue
        if fingerprint(candidate) == PICTURE_SHA256:
            return candidate
        print("warning: %s is not the entered picture" % name,
              file=sys.stderr)
    for candidate in sorted(folder.glob("*.png")):
        if candidate.name in CANDIDATE_NAMES:
            continue
        if candidate.is_file() \
                and fingerprint(candidate) == PICTURE_SHA256:
            print("note: the entered picture was found under the "
                  "unexpected name %s" % candidate.name, file=sys.stderr)
            return candidate
    raise FileNotFoundError(
        "the entered picture is not in %s" % directory)


def publish_location():
    """Return where the picture must be published.

    The grader names the directory in MAKEFUN_OUTPUT_DIR; the
    plain /output directory is next; as a last resort the picture
    is published next to this program.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir and os.path.isdir("/output"):
        out_dir = "/output"
    if not out_dir:
        out_dir = str(Path(__file__).resolve().parent)
    return Path(out_dir) / "entry.png"


def publish():
    here = Path(__file__).resolve().parent
    source = locate_picture(here)
    picture = source.read_bytes()

    width, height = picture_dimensions(picture)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("the entered picture is %dx%d, over the "
                         "1024x1024 limit" % (width, height))
    if len(picture) > MAX_BYTES:
        raise ValueError("the entered picture is %d bytes, over "
                         "the 1 MiB limit" % len(picture))
    if hashlib.sha256(picture).hexdigest() != PICTURE_SHA256:
        raise IOError("the bytes read do not match the entered "
                      "picture")

    target = publish_location()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(picture)

    # Read the published file back and check it once more. A short
    # or corrupted write must fail loudly here, not at judging time.
    if fingerprint(target) != PICTURE_SHA256:
        raise IOError("the published file does not match the "
                      "entered picture")

    print("published %s (%d bytes, %dx%d) to %s"
          % (source.name, len(picture), width, height, target))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(publish())
    except (FileNotFoundError, ValueError, IOError, OSError) as exc:
        # A missing picture, a wrong fingerprint, or a failed write
        # is an entry problem, not a crash: say so plainly and
        # leave with a non-zero status instead of a traceback.
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(1)
