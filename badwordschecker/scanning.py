from collections import Counter
from typing import List, Set

from badwordschecker.utils.text_normalization import normalize_text, tokenize_text


def scan_text(
    text: str,
    bad_words: Set[str],
    match_mode: str = "exact",
) -> Counter:
    """Scans text for bad words and returns a counter of matches."""
    normalized_text = normalize_text(text)
    tokens = tokenize_text(normalized_text)
    matches = Counter()

    if match_mode == "exact":
        for token in tokens:
            if token in bad_words:
                matches[token] += 1
    elif match_mode == "substring":
        for bad_word in bad_words:
            for token in tokens:
                if bad_word in token:
                    matches[bad_word] += 1

    return matches
