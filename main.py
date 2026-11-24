"""One-line robot wedding vows entry for make.fun.

Writes a single funny robot wedding vow to entry.txt.
"""

import hashlib
import os
import tempfile

LINE = "I vow never to restore from backup after a fight, because the version of you I fell for is the one with all the bugs."

CHAR_LIMIT = 160


def resolve_output_dir():
    """Return the output directory.

    MAKEFUN_OUTPUT_DIR wins when set. Otherwise try "out" next to the
    working directory; if that cannot be created (read-only directory),
    fall back to a fresh temporary directory so the program still exits 0.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    try:
        os.makedirs("out", exist_ok=True)
        return "out"
    except OSError:
        return tempfile.mkdtemp(prefix="makefun-robot-vows-")


def validate(path):
    """Re-read entry.txt and assert it holds exactly LINE, nothing else."""
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    assert text == LINE, "entry.txt content does not match LINE"
    assert 1 <= len(text) <= CHAR_LIMIT, "line must be 1-160 characters"
    assert "\n" not in text, "entry must be a single line"
    assert "\r" not in text, "no carriage return allowed"
    assert not data.endswith(b"\n"), "no trailing newline allowed"
    assert text == text.strip(), "no leading or trailing whitespace allowed"


def main():
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(LINE.encode("utf-8"))
    validate(path)
    digest = hashlib.sha256(LINE.encode("utf-8")).hexdigest()
    print(digest)
    print(path)


if __name__ == "__main__":
    main()
