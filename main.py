"""Two-Sentence Horror — make.fun entry.

Writes one original two-sentence horror story to
$MAKEFUN_OUTPUT_DIR/entry.txt (default ./output/entry.txt).

Gate (from the competition rules): the file must be UTF-8 text of
1 to 400 characters, not only white space. The story itself is
exactly two sentences, original fiction, no real person's name.
"""

import os
import re
import sys

STORY = (
    "The shelter said the dog I adopted flinches at raised voices, "
    "so for a month I have spoken to him only in whispers. "
    "Last night he finally spoke \u2014 in my voice, "
    "saying the words I had only thought."
)

MAX_CHARS = 400
MIN_CHARS = 1
EXPECTED_SENTENCES = 2


def resolve_output_dir():
    """Return the output directory, honouring MAKEFUN_OUTPUT_DIR."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.getcwd(), "output")


def count_sentences(text):
    """Count sentences by terminal punctuation (. ! ?), ignoring
    ellipses and decimal points."""
    cleaned = re.sub(r"\.{2,}", "", text)
    cleaned = re.sub(r"(?<=\d)\.(?=\d)", "", cleaned)
    return len(re.findall(r"[.!?]", cleaned))


def validate(text):
    """Enforce the competition gate: 1-400 chars, not only
    whitespace, exactly two sentences, single-line clean text."""
    if not isinstance(text, str):
        raise ValueError("story must be a string")
    if not text.strip():
        raise ValueError("story must not be only white space")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        raise ValueError(
            "story must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if "\n" in text or "\r" in text:
        raise ValueError("story must be a single line of text")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("story must not contain control characters")
    n = count_sentences(text)
    if n != EXPECTED_SENTENCES:
        raise ValueError(
            "story must be exactly %d sentences, got %d"
            % (EXPECTED_SENTENCES, n)
        )
    return True


def main():
    validate(STORY)
    # Round-trip through UTF-8: the gate reads the file as UTF-8 text.
    STORY.encode("utf-8").decode("utf-8")
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(STORY)
    print("wrote %s (%d chars, %d sentences)"
          % (path, len(STORY), count_sentences(STORY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
