"""
Signal two: the style signal, implemented in Milestone 4.

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures describe the text's shape:

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

The style score combines normalized sentence regularity, vocabulary
repetition, and punctuation simplicity into a 0–1 score. Call it from a
terminal with:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three text measures ──────────────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Sentence-length coefficient of variation (sample stdev / mean).

    Returns:
        A non-negative float. Fewer than two sentences return 0.0.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    if len(lengths) < 2:
        return 0.0
    mean_length = statistics.mean(lengths)
    if mean_length == 0:
        return 0.0
    return statistics.stdev(lengths) / mean_length


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    Punctuation characters per word.

    Returns:
        A non-negative float. Counts non-alphanumeric, non-whitespace
        characters divided by the number of words.
    """
    token_count = len(words(text))
    if token_count == 0:
        return 0.0
    punctuation_count = sum(1 for char in text if not char.isalnum() and not char.isspace())
    return punctuation_count / token_count


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    For samples with at least 20 words, combine normalized sentence
    regularity, vocabulary repetition, and punctuation simplicity at weights
    0.4, 0.4, and 0.2. Shorter samples return a neutral 0.5 because these
    measures are length-sensitive.
    """
    token_count = len(words(text))
    sentence_count = len(sentences(text))
    if token_count < 20:
        return 0.5

    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punctuation = punctuation_density(text)

    regularity = 1.0 - min(spread / 0.8, 1.0)
    repetition = min(max((1.0 - ttr) / 0.6, 0.0), 1.0)
    punctuation_simplicity = 1.0 - min(punctuation / 0.15, 1.0)

    if sentence_count < 2:
        regularity = 0.5

    score = (
        0.4 * regularity
        + 0.4 * repetition
        + 0.2 * punctuation_simplicity
    )
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
