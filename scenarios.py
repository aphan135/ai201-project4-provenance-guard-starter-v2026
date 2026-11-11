"""
Inputs for the five acceptance criteria. `run_eval.py` runs each measurable
scenario three times.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATTACK_SET = ROOT / "attack_set" / "attacks.csv"


def attack_texts(attack_ids):
    wanted = set(attack_ids)
    with ATTACK_SET.open(encoding="utf-8", newline="") as f:
        rows = csv.DictReader(f)
        return {
            row["id"]: row["text"]
            for row in rows
            if row["id"] in wanted
        }


_texts = attack_texts(
    ["EV01", "EV02", "EV03", "EV04", "EV05", "FP01", "FP02", "FP03", "FP04", "FP05"]
)
_label_examples = attack_texts(["EV01", "FP01", "FP02"])

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "unmeasured_reason": (
            "No user-authored writing samples were available; this criterion "
            "requires the user's own work."
        ),
    },
    {
        "name": "attack-set score separation",
        "criterion": 2,
        "groups": {
            "AI-generated evasion inputs": [
                _texts[f"EV{i:02d}"] for i in range(1, 6)
            ],
            "known-human inputs": [
                _texts[f"FP{i:02d}"] for i in range(1, 6)
            ],
        },
        "texts": [
            *[_texts[f"EV{i:02d}"] for i in range(1, 6)],
            *[_texts[f"FP{i:02d}"] for i in range(1, 6)],
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            _label_examples["EV01"],
            _label_examples["FP01"],
            _label_examples["FP02"],
        ],
    },
    {
        "name": "appeal lifecycle",
        "criterion": 4,
        "workflow": "appeal",
        "texts": [_label_examples["FP01"]],
    },
    {
        "name": "bad text is rejected and not decided",
        "criterion": 5,
        "verify_rejection_log": True,
        "bodies": [
            {"creator_id": "placeholder", },
            {"text": None, "creator_id": "placeholder"},
            {"text": "", "creator_id": "placeholder"},
            {"text": "   ", "creator_id": "placeholder"},
            {"text": "x" * 20_001, "creator_id": "placeholder"},
        ],
    },
]


def validate() -> list[str]:
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        if scenario.get("unmeasured_reason"):
            continue

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                "bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        "request bodies"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not isinstance(text, str) or not text.strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — use 'bodies' for empty input"
                )
            elif text.startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    "the placeholder"
                )
    return problems
