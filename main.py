#!/usr/bin/env python3
"""Publisher for the v16 entry to make.fun's news-image-20261124.

The deliverable is a single picture: entry.png, stored next to this
file, a 1024x1024 broadsheet page that sums up the world news of
Tuesday 24 November 2026. Running this program copies that picture
into the output directory as entry.png — but only once the stored
file's SHA-256 digest matches the digest recorded below, so a
damaged or swapped image is turned away instead of published.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = (
    "7b87897617a942293df9bc9eb881caa8410f5f3895d6edcaad9fd91a9f373e87"
)
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_of(data):
    return hashlib.sha256(data).hexdigest()


def read_source():
    with open(SOURCE, "rb") as fh:
        return fh.read()


def main():
    data = read_source()
    if not data:
        print("nothing to publish: %s is empty" % SOURCE,
              file=sys.stderr)
        return 1
    digest = sha256_of(data)
    if digest != EXPECTED_SHA256:
        print("refusing to publish: sha256 %s does not match the "
              "recorded %s" % (digest, EXPECTED_SHA256),
              file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Publish atomically rather than writing the target in place:
    # stage the bytes in a scratch file in the same directory, flush
    # them to disk, check what actually landed, and only then rename
    # over the target. An interrupted run can leave a stray scratch
    # file behind, but never a half-written entry.png.
    scratch = TARGET + ".part"
    with open(scratch, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    with open(scratch, "rb") as fh:
        staged = fh.read()
    if sha256_of(staged) != EXPECTED_SHA256:
        print("staged copy failed verification, discarding: %s"
              % scratch, file=sys.stderr)
        os.unlink(scratch)
        return 1
    os.replace(scratch, TARGET)

    with open(TARGET, "rb") as fh:
        published = fh.read()
    if sha256_of(published) != EXPECTED_SHA256:
        print("published copy failed its read-back check: %s" % TARGET,
              file=sys.stderr)
        return 1

    print("published %s (%d bytes, sha256 %s)"
          % (TARGET, len(published), EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
