#!/usr/bin/env python3
"""Publisher for the news-image-20261124 entry.

The judged artwork for this entry is a single PNG stored next to this
file as ``entry.png``.  Running this program places a copy of that
picture in the grading output directory and proves, with a SHA-256
digest, that the bytes which landed there are exactly the bytes that
were submitted.  Any mismatch aborts the run with a non-zero exit
code so a corrupted or truncated copy can never pass silently.

Only the Python standard library is used.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

# SHA-256 of the approved entry.png, recorded when the image was
# finalised.  The published copy must hash to this exact value.
EXPECTED_SHA256 = "7b87897617a942293df9bc9eb881caa8410f5f3895d6edcaad9fd91a9f373e87"

IMAGE_NAME = "entry.png"
CHUNK = 65536


def digest_of(path):
    """Return the SHA-256 hex digest of the file at ``path``."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def output_directory():
    """Where the grader expects the entry: MAKEFUN_OUTPUT_DIR or /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen) if chosen else Path("/output")


def fail(message, code):
    print("error: " + message, file=sys.stderr)
    return code


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        return fail("stored image missing: %s" % source, 2)

    # The stored artwork itself must match the recorded digest before
    # anything is published; otherwise the repo contents are wrong.
    stored_digest = digest_of(source)
    if stored_digest != EXPECTED_SHA256:
        return fail(
            "stored image digest %s does not match the recorded %s"
            % (stored_digest, EXPECTED_SHA256),
            1,
        )

    target_dir = output_directory()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME

    # Publish atomically: copy to a scratch file in the same directory,
    # flush it to disk, verify its digest, and only then rename it over
    # the final name.  An interrupted run can therefore never leave a
    # half-written entry.png behind for the grader to pick up.
    scratch = target_dir / (IMAGE_NAME + ".part")
    try:
        with open(source, "rb") as src, open(scratch, "wb") as dst:
            shutil.copyfileobj(src, dst, CHUNK)
            dst.flush()
            os.fsync(dst.fileno())

        published_digest = digest_of(scratch)
        if published_digest != EXPECTED_SHA256:
            return fail(
                "staged copy digest %s does not match the recorded %s"
                % (published_digest, EXPECTED_SHA256),
                1,
            )
        os.replace(scratch, target)
    finally:
        if scratch.exists():
            scratch.unlink()

    print(published_digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
