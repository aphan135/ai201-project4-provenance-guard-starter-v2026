"""
Combining the two signals and mapping a score to a reader-facing label.

`combine_signals` is implemented in Milestone 4. `score_to_label` remains a
Milestone 5 stub.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score.

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    The weighted average uses the configured model/style weights. A large
    disagreement returns 0.5 so neither signal alone makes a confident claim.
    """
    if not 0.0 <= model_score <= 1.0 or not 0.0 <= style_score <= 1.0:
        raise ValueError("Signal scores must be between 0.0 and 1.0.")

    if abs(model_score - style_score) >= config.MAX_SIGNAL_DISAGREEMENT:
        return 0.5

    weight_total = config.WEIGHT_MODEL_SIGNAL + config.WEIGHT_STYLE_SIGNAL
    if weight_total <= 0.0:
        raise ValueError("Signal weights must have a positive sum.")
    score = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    ) / weight_total
    return round(min(max(score, 0.0), 1.0), 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a combined score into a guess and reader-facing sentence.

    Returns:
        A machine-readable guess (`human`, `unsure`, or `ai`) and its
        full reader-facing label.
    """
    if not 0.0 <= score <= 1.0:
        raise ValueError("Combined score must be between 0.0 and 1.0.")
    if score >= config.AI_THRESHOLD:
        return (
            "ai",
            "We think this was probably written by AI, but this estimate is "
            "not proof of authorship.",
        )
    if score <= config.HUMAN_THRESHOLD:
        return (
            "human",
            "We think this was probably written by a person.",
        )
    return (
        "unsure",
        "We can't tell who wrote this from the text alone. If you wrote it, "
        "this result is not an accusation.",
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f} inclusive"),
        (
            "unsure",
            f"above {config.HUMAN_THRESHOLD:.2f} and below {config.AI_THRESHOLD:.2f}",
        ),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00 inclusive"),
    ]
