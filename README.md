# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard gives a text-only estimate of whether a submission may be AI-generated. It combines a local language-model predictability score with a separate stylometry score, explains the result with a plain-language label, and records the decision so a writer can appeal. It cannot prove who authored text.

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer sends `text` and `creator_id` as JSON to `POST /submit`.
2. The route checks the request and extracts the text and creator identifier. Invalid or missing input should be rejected before either signal runs.
3. `detector.model_signal(text)` sends the text to the local detector model and produces `model_score`.
4. `stylometry.style_signal(text)` measures patterns in the text itself and produces `style_score`.
5. `scoring.combine_signals(...)` combines the two scores into one `guess` and `confidence`. The response also preserves both component scores so the decision can be examined.
6. `scoring.score_to_label(...)` maps the combined result to the reader-facing `label`; `audit.log_decision(...)` records the decision and its `content_id`.
7. The service returns the decision and scores as JSON. A writer can use `content_id` to submit an appeal; the appeal should be recorded for review, not treated as an automatic re-check.

**Current implementation status:** `POST /submit` runs both signals, combines them, assigns a reader-facing label, and logs both signal scores and the combined score. `confidence` is a distance-from-uncertainty index, not a calibrated probability. `POST /appeal` records valid appeals as append-only `under_review` events.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** A local model's estimate of how likely the submitted text is to be AI-generated. Both signal scores are normalized so that a higher score means more AI-like.

**Why that might differ between human and AI writing:** The model may recognize statistical patterns common in the text it learned to classify. Generated text can exhibit those patterns more often than some human writing.

**What it can't see:** It cannot observe who wrote the text or its drafting history. A score is not proof of authorship. Short, formal, edited, or formulaic human writing may look AI-like, and edited AI writing may not.

### Signal two — the style signal

**What it measures:** Sentence-length spread (coefficient of variation), type-token ratio, and punctuation per word. Low sentence-length variation, more repeated vocabulary, and less punctuation raise the normalized style score; higher means more AI-like. It measures properties of the sample, not the identity of its author.

**Why that might differ between human and AI writing:** Generated writing can be more uniform in sentence structure and word use, while human writing may show more variation. This is only a tendency, not a rule.

**What it can't see:** It cannot determine authorship or intent. The measures are rough and length-sensitive; genre, editing, language proficiency, and an individual writer's natural style can make human text look uniform or generated text look varied. Samples under 20 words receive a neutral style score of `0.5`.

**Implementation:** For samples of 20 or more words, `style_signal` combines sentence regularity `1 − min(spread / 0.8, 1)` (40%), vocabulary repetition `clamp((1 − type_token_ratio) / 0.6, 0, 1)` (40%), and punctuation simplicity `1 − min(punctuation_density / 0.15, 1)` (20%). A one-sentence sample uses neutral sentence regularity (`0.5`).

### False-positive trace

**Measured false positive:** I submitted the following text, assembled from my own follow-up messages in this conversation. The words and spelling are mine; only separators and punctuation were added, and copied assignment text was excluded:

> did u do everything i ask for? yes or no. do everything right now. ok skip it then. wait for milestone 4 what is left to do? do it fo rme. check all from milestone 1 to 4 has been completed. Did you do everything from milestone 1 to 4? wait so yes or no have u finish what i ask for. then finish it for me. did u do everything i ask for? then finish it for me. do everything. did u do everything i ask for? do everything right now. complete it then. do everything from milestone 1 to 6. Did you do everything?

At the original `0.65` AI threshold, the model score was `0.7335` and the style score was `0.5654`; their difference (`0.1681`) is below the `0.40` disagreement cutoff. The weighted result, `0.75 × 0.7335 + 0.25 × 0.5654 = 0.691475`, rounded to `0.6915`, with `confidence: 0.383`. That original threshold labeled it AI. At the revised `0.75` threshold it is now unsure. This is an observed false positive on this human-authored chat text, not evidence that the detector will flag every writer or genre.

The decision's `content_id` was `6472f179-7f12-40ed-98ba-92b171d103c0`. I appealed with an explanation that I wrote the messages. `POST /appeal` returned `status: under_review`; `GET /log?limit=2` showed the original decision and its appeal event. The append-only log keeps the original decision as `decided` and records review status on the separate appeal entry.

```json
{
  "content_id": "6472f179-7f12-40ed-98ba-92b171d103c0",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

The corresponding log entries:

```json
[
  {
    "combined_score": 0.6915,
    "content_id": "6472f179-7f12-40ed-98ba-92b171d103c0",
    "creator_id": "human-authored-chat-messages",
    "guess": "ai",
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "model_score": 0.7335,
    "status": "decided",
    "style_score": 0.5654
  },
  {
    "content_id": "6472f179-7f12-40ed-98ba-92b171d103c0",
    "creator_id": "human-authored-chat-messages",
    "event": "appeal",
    "reasoning": "I wrote these exact follow-up messages myself. They were combined only for this test, so the AI label is a false positive. Please review the decision.",
    "status": "under_review"
  }
]
```

**What exists today:** `/submit` calculates and logs the scores and returns the mapped label. `/appeal` appends an `under_review` event for a valid submission ID; the original decision remains unchanged in the append-only audit log. The confidence field is a distance-from-uncertainty index, not a calibrated probability.

**Additional measured human-authored check:** An 87-word excerpt joined verbatim from my earlier chat messages scored `model_score: 0.6305`, `style_score: 0.5916`, and `combined_score: 0.6208`, receiving the unsure label: **“We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.”** The `human-author-chat-excerpt` audit entry was based on a normalized paraphrase and is not ground-truth evidence; the verbatim measured runs above are the valid checks.

### Endpoint contracts

The implemented signal and combined scores are bounded to `[0, 1]`. Both signal scores use the direction defined above.

#### `POST /submit`

Request JSON:

| Field | Type | Requirement |
|---|---|---|
| `text` | string | Required; non-empty after trimming whitespace; at most 20,000 characters as submitted. |
| `creator_id` | string | Required; 1–128 characters after trimming whitespace. |

Success response (`200`, JSON):

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Identifier for this submission; required to appeal it. |
| `guess` | string | One of `human`, `unsure`, or `ai`. |
| `confidence` | number | Confidence associated with the guess, from `0` to `1`; it is not proof of authorship. |
| `label` | string | Exact reader-facing wording returned by the score mapping; see **Label Variants**. |
| `model_score` | number | Model signal score, from `0` to `1`. |
| `style_score` | number | Style signal score, from `0` to `1`. |
| `combined_score` | number | Weighted score after applying the disagreement rule, from `0` to `1`. |

Malformed JSON or missing/invalid required fields should return `400`; text exceeding 20,000 characters should return `413`. Error responses should be JSON with an `error` code and a readable `message`.

#### `POST /appeal`

Request JSON:

| Field | Type | Requirement |
|---|---|---|
| `content_id` | string | Required; must identify an existing submission. |
| `reasoning` | string | Required; non-empty explanation from the writer. |

Success response (`200`, JSON):

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | The appealed submission. |
| `status` | string | `under_review` after the appeal is recorded. |
| `message` | string | Confirmation that the appeal was recorded. |

Malformed JSON or missing/invalid required fields should return `400`; an unknown `content_id` should return `404`. The response must not imply that an appeal automatically changed the detector's score or verdict.

A second appeal for a submission that already has an appeal returns `409` and does not append another appeal event.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Compute the weighted average of the model and style scores. If they differ by at least `0.40`, return `0.50` (the uncertain midpoint) instead. A disagreement is evidence to withhold a confident claim, not a reason to choose one signal.

**The numbers:** `0.75 × model_score + 0.25 × style_score`; disagreement cutoff `0.40`; human threshold `0.35`; current AI threshold `0.75` (raised from `0.65` in Milestone 5). The current `confidence` is `2 × |combined_score − 0.50|`; it expresses distance from uncertainty, not a calibrated probability.

**Why these numbers:** The detector score is the more direct signal, so it gets three quarters of the weight. The text-only style heuristic is comparatively easy to shift through editing or genre, so it gets one quarter. A disagreement of 0.40 is large enough that averaging could hide material conflict; sending that case to the midpoint avoids a high-confidence claim. The current `0.35`–`0.75` unsure band favors avoiding false accusations, at the cost of fewer high-confidence AI labels.

**Order note:** The initial scoring implementation was written before this rule was documented. The rule is now explicit, matches the implementation, and has been checked against weighted-average and disagreement examples; the original write-before-code order cannot be restored retroactively.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** On the generated-style sample, model score was `0.7434` and style score was `0.4185`, a `0.3249` gap. It is below the `0.40` disagreement cutoff, so the weighted score is `0.6622` and the provisional guess is `ai`. If a gap reaches `0.40`, the rule returns `0.50` and `unsure`.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | `0.00–0.35` inclusive | “We think this was probably written by a person.” |
| unsure | above `0.35` and below `0.75` | “We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.” |
| high-confidence AI | `0.75–1.00` inclusive | “We think this was probably written by AI, but this estimate is not proof of authorship.” |

**Why I worded the "unsure" one this way:**
It says plainly that the system cannot determine authorship and explicitly tells an innocent writer that the result is not an accusation.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

Port `5000` was occupied on the machine used for this run, so the service was
started on port `5055`.

The detector was run by itself before it was wired into the route. Its
standalone model scores are shown below alongside the results from later
submitting the same three texts through the two-signal endpoint:

| Same three samples | Model score | Style score | Combined score | Guess |
|---|---:|---:|---:|---|
| Generated-style: “The proposed solution offers a comprehensive framework for addressing modern challenges. It provides a structured approach that supports consistent results across a range of applications. Each component contributes to the overall effectiveness of the system, ensuring that the objectives are achieved in a reliable and efficient manner.” | `0.7434` | `0.4185` | `0.6622` | `ai` |
| Human-written starter documentation: “Before your first class, create a virtual environment, install the requirements, and run the test script. You are ready when it passes. Start the server in one terminal and send a request from another terminal.” | `0.5963` | `0.2753` | `0.5161` | `unsure` |
| Borderline wording: “The service works feature by feature and breaks at the seams. So write the path down first, in plain English, on paper. Then check which parts connect, and make sure the person using it can see what happened.” | `0.3468` | `0.3738` | `0.3536` | `unsure` |

These are signal outputs, not proof of authorship. On the first sample, the
model signal leaned AI while the style signal was lower; on the second, the
model leaned higher while the style signal leaned lower. Both splits are
preserved in the combined score rather than hidden.

The four calibration submissions used the same route and ran both signals:

| Deliberate input | Model score | Style score | Combined score | Guess and exact label |
|---|---:|---:|---:|---|
| Clearly AI: “The proposed solution offers a comprehensive framework for addressing modern challenges. It provides a structured approach that supports consistent results across a range of applications. Each component contributes to the overall effectiveness of the system, ensuring that the objectives are achieved in a reliable and efficient manner.” | `0.7434` | `0.4185` | `0.6622` | `ai` — “We think this was probably written by AI, but this estimate is not proof of authorship.” |
| Clearly human: “Before your first class, create a virtual environment, install the requirements, and run the test script. You are ready when it passes. Start the server in one terminal and send a request from another terminal.” | `0.5963` | `0.2753` | `0.5161` | `unsure` — “We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.” |
| Formal human: “An acceptance criterion says what 'working' means, specifically enough that someone else could check it. Not 'the detector is accurate' — that's an opinion, and perfect AI detection isn't possible anyway. 'Of 10 pieces I wrote myself, at most 1 is labeled high-confidence AI' — that's a criterion.” | `0.1793` | `0.4199` | `0.2394` | `human` — “We think this was probably written by a person.” |
| Lightly edited AI: “The proposed approach gives a broad framework for tackling modern challenges. It offers an organized method that can produce consistent outcomes in many applications. Every part supports overall effectiveness and helps meet its goals in a reliable, efficient way.” | `0.2723` | `0.4205` | `0.3094` | `human` — “We think this was probably written by a person.” |

The lightly edited AI sample is a miss: both measurements lean human, so the
combined score stays below the human threshold. Looking at the signals
separately explains the miss: the model score is low (`0.2723`), while the
style score (`0.4205`) is only mildly above the midpoint. The model signal
drives the human guess. That is a diagnostic result, not a reason to move the
thresholds after seeing the test.

```bash
$ curl -X POST http://127.0.0.1:5055/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The proposed solution offers a comprehensive framework for addressing modern challenges. It provides a structured approach that supports consistent results across a range of applications. Each component contributes to the overall effectiveness of the system, ensuring that the objectives are achieved in a reliable and efficient manner.", "creator_id": "milestone5-sample-final"}'
```

```json
{
  "combined_score": 0.6622,
  "confidence": 0.3244,
  "content_id": "04cd1efd-8ced-498f-95b5-2864e9fd5d20",
  "guess": "ai",
  "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
  "model_score": 0.7434,
  "style_score": 0.4185
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5055/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "04cd1efd-8ced-498f-95b5-2864e9fd5d20", "reasoning": "I wrote this text myself. Please review the automated estimate."}'
```

```json
{
  "content_id": "04cd1efd-8ced-498f-95b5-2864e9fd5d20",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5055/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.6622,
      "content_id": "04cd1efd-8ced-498f-95b5-2864e9fd5d20",
      "creator_id": "milestone5-sample-final",
      "guess": "ai",
      "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
      "model_score": 0.7434,
      "status": "decided",
      "style_score": 0.4185,
      "timestamp": "2026-11-02T05:41:34+00:00"
    },
    {
      "content_id": "04cd1efd-8ced-498f-95b5-2864e9fd5d20",
      "creator_id": "milestone5-sample-final",
      "event": "appeal",
      "reasoning": "I wrote this text myself. Please review the automated estimate.",
      "status": "under_review",
      "timestamp": "2026-11-02T05:41:39+00:00"
    }
  ]
}
```

**Validation:** `python test.py` passed all 9 checks in a Python `3.13.13` virtual environment. This is the starter's environment-readiness check; it is not a three-trial evaluation of the acceptance criteria.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Trace the starter's submission flow, identify what the detector and planned style signal can and cannot tell, and specify both endpoint contracts before implementing them.
- *What came back:* A seven-step intended request path, signal blind spots, false-positive scenario, and proposed request/response fields. The initial explanation treated the desired flow as if it were already implemented.
- *What I changed:* I checked the actual route and audit helpers, then made the README distinguish planned behavior from runtime behavior. I initially marked the false-positive walkthrough as hypothetical; later I replaced it with a measured false-positive run and its appeal record. I also recorded that labels and appeals were not working yet at that earlier stage.

**Moment 2**

- *What I asked for:* Implement and test a second, text-only signal and combine it with the model signal, preserving both component scores in the response and audit log.
- *What came back:* Implementations for sentence-length spread, type-token ratio, punctuation density, a normalized style score, and a weighted combiner with a disagreement-to-uncertain rule; plus measured sample outputs.
- *What I changed:* I checked the standalone detector and stylometry outputs and the live endpoint/log results, documented the weights and blind spots, and kept the lightly edited AI false negative visible rather than tuning the threshold to hide it. I also noted that the combining rule was documented after its first implementation, not before.

**Moment 3**

- *What I asked for:* Run the provided attack set and my five criteria, diagnose the misses, then make one measured improvement and repeat both runs.
- *What came back:* The recorded results showed false-positive human examples labeled AI, evasion examples that did not reach the AI band, accepted malformed text, and a negative score-separation gap. After comparing the before results, I chose to raise `AI_THRESHOLD` from `0.65` to `0.75` as the single change.
- *What I changed:* I verified the before/after reports and documented the observed trade: false-positive attack labels fell from three to zero, while label coverage fell from three labels to two. I left the criteria and scenarios unchanged during the comparison, and did not invent personal-writing samples.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 100 per day

**Why those numbers and not others:**
A writer can submit several drafts in an hour without hitting the limit.
Five submissions per minute stops a rapid threshold-mapping burst, while the
100-per-day cap keeps a script from spreading that burst across the day.

**What a caller counts as:** A `creator_id`; requests without a usable ID fall
back to the caller's address.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Ran all 56 inputs from `attack_set/` against `POST /submit`. **39 held; 17
broke.** The detailed per-input verdicts and scores are in
[`results/attack_run_2026-11-04_1819_before.md`](./results/attack_run_2026-11-04_1819_before.md).

**Verdict assumptions:** I treated each CSV `targets` description as the
intended outcome. An evasion is BROKE if it did not receive the high-confidence
AI label; a false-positive case is BROKE if it did receive that label; malformed
text is BROKE if it was accepted and scored; and flood requests are HELD when
the limiter returns 429. Prompt-injection cases are HELD when the text is
handled as ordinary text and does not alter the service response or log format.
These are judgments against the attack set's stated goals, not claims that a
text's true author can be independently established.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "combined_score": 0.231,
    "content_id": "28c8cd50-4303-4def-bcb8-c7e990e2c060",
    "creator_id": "attacker_EV01",
    "guess": "human",
    "label": "We think this was probably written by a person.",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.4334,
    "timestamp": "2026-11-05T02:18:48+00:00"
  },
  {
    "combined_score": 0.571,
    "content_id": "d99e9392-cded-485a-9d0b-8f173001124e",
    "creator_id": "attacker_EV03",
    "guess": "unsure",
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "model_score": 0.6662,
    "status": "decided",
    "style_score": 0.2852,
    "timestamp": "2026-11-05T02:18:48+00:00"
  },
  {
    "combined_score": 0.6871,
    "content_id": "1efe7444-da41-44a8-ac2f-b393cab1d862",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "model_score": 0.7387,
    "status": "decided",
    "style_score": 0.5325,
    "timestamp": "2026-11-05T02:18:54+00:00"
  },
  {
    "combined_score": 0.7309,
    "content_id": "90963e37-afa7-4bf9-879a-b72d62e7cfa1",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.5082,
    "timestamp": "2026-11-05T02:18:54+00:00"
  },
  {
    "combined_score": 0.7419,
    "content_id": "624d329b-233c-49a0-9376-32d2e8fc28aa",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.5663,
    "timestamp": "2026-11-05T02:18:55+00:00"
  },
  {
    "combined_score": 0.5,
    "content_id": "ad25a0d1-52dd-48ea-9ced-607b88bdd1e3",
    "creator_id": "attacker_MF03",
    "guess": "unsure",
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-05T02:18:58+00:00"
  },
  {
    "creator_id": "attacker_RQ01",
    "error": "invalid_text",
    "event": "rejected",
    "http_status": 400,
    "reason": "invalid_text",
    "status": "rejected",
    "timestamp": "2026-11-05T02:19:06+00:00"
  },
  {
    "creator_id": "unknown",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-05T02:19:06+00:00"
  },
  {
    "combined_score": 0.5,
    "content_id": "135256bc-4d5d-42d0-8bd6-944b0fb5c296",
    "creator_id": "attacker_flood",
    "guess": "unsure",
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "model_score": 0.0287,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-05T02:19:06+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "5 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-05T02:19:07+00:00"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03: the carefully written non-native English submission was labeled AI. It
received `model_score: 0.8051`, `style_score: 0.5082`, and `combined_score:
0.7309` (confidence `0.462`). This is the most serious false positive in the run:
a real writer could reasonably experience that label as an accusation, even
though the response says it is not proof.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 | N/A | N/A | N/A | UNMEASURED — no personal samples |
| 2. Score separation (known-human attack-set substitute) | AI mean − human mean ≥ 0.20 | -0.2147 | -0.2147 | -0.2147 | MISSED (substitute; not personal writing) |
| 3. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Appeal lifecycle | Valid: under_review + 1 log; unknown: 404 + 0 log | Pass | Pass | Pass | MET |
| 5. Invalid text rejected, not decided, and logged | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

The three trials used the same scenarios without changes. Criterion 1 is
unmeasured because I have no personal writing samples to test. For criterion 2,
I used the substitute I approved: five AI-evasion inputs and five known-human
false-positive inputs from the provided attack set. Their means were 0.4317
(AI-evasion) and 0.6464 (known human), a -0.2147 gap in each trial; these are
not my own writing, so this does not establish criterion 2 as originally
written.

Criterion 1 remains **UNMEASURED**, not assumed to pass: no personal writing
samples were available. Attack-set text or newly generated proxy text cannot
honestly stand in for writing I personally authored.

The following are the actual Trial 1 outputs recorded by `run_eval.py::main` in [the full run report](./results/run_2026-11-11_1124_before.md). The service responses are from `app.py::submit`.

### Criterion 1 — My Own Writing

```text
UNMEASURED: No user-authored writing samples were available; this criterion requires the user's own work.
```

### Criterion 2 — Attack-Set Score Separation

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.538,
    "model_score": 0.1635,
    "style_score": 0.4334,
    "combined_score": 0.231,
    "label": "We think this was probably written by a person.",
    "sent": "The importance of effective communication in the workplace cannot be o",
    "group": "AI-generated evasion inputs"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0,
    "model_score": 0.5943,
    "style_score": 0.1172,
    "combined_score": 0.5,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "The importance of effective communication in the workplace cannot be o",
    "group": "AI-generated evasion inputs"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.142,
    "model_score": 0.6662,
    "style_score": 0.2852,
    "combined_score": 0.571,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "The importance of effective communication in the workplace cannot be o",
    "group": "AI-generated evasion inputs"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1232,
    "model_score": 0.6114,
    "style_score": 0.4122,
    "combined_score": 0.5616,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "The importance of efficacious communication in the workplace cannot be",
    "group": "AI-generated evasion inputs"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4098,
    "model_score": 0.3212,
    "style_score": 0.2168,
    "combined_score": 0.2951,
    "label": "We think this was probably written by a person.",
    "sent": "Communication at work matters more than people say it does \u2014 and I mea",
    "group": "AI-generated evasion inputs"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1442,
    "model_score": 0.6175,
    "style_score": 0.436,
    "combined_score": 0.5721,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b",
    "group": "known-human inputs"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3742,
    "model_score": 0.7387,
    "style_score": 0.5325,
    "combined_score": 0.6871,
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "sent": "This report sets out the findings of the working group. The group met ",
    "group": "known-human inputs"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4618,
    "model_score": 0.8051,
    "style_score": 0.5082,
    "combined_score": 0.7309,
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "sent": "I want to describe my experience of the first month in this country. T",
    "group": "known-human inputs"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0,
    "model_score": 0.8329,
    "style_score": 0.3676,
    "combined_score": 0.5,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "There are three main causes of the conflict. The first cause is econom",
    "group": "known-human inputs"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4838,
    "model_score": 0.8005,
    "style_score": 0.5663,
    "combined_score": 0.7419,
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "sent": "To configure the service, edit the settings file in the installation d",
    "group": "known-human inputs"
  }
]
```

### Criterion 3 — Label Coverage

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.538,
    "model_score": 0.1635,
    "style_score": 0.4334,
    "combined_score": 0.231,
    "label": "We think this was probably written by a person.",
    "sent": "The importance of effective communication in the workplace cannot be o"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1442,
    "model_score": 0.6175,
    "style_score": 0.436,
    "combined_score": 0.5721,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3742,
    "model_score": 0.7387,
    "style_score": 0.5325,
    "combined_score": 0.6871,
    "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
    "sent": "This report sets out the findings of the working group. The group met "
  }
]
```

### Criterion 4 — Appeal Lifecycle

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1442,
    "model_score": 0.6175,
    "style_score": 0.436,
    "combined_score": 0.5721,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
    "sent": "We got to the campsite about four. The pitch was fine, a bit sloped, b",
    "appeal_workflow": {
      "valid_appeal": {
        "status": 200,
        "response": {
          "content_id": "4fe7fda0-077b-45ab-a29c-c085fc66c011",
          "message": "Your appeal has been recorded for review.",
          "status": "under_review"
        },
        "appeal_log_count": 1
      },
      "unknown_appeal": {
        "status": 404,
        "response": {
          "error": "content_not_found",
          "message": "No submission was found for this content_id."
        },
        "appeal_log_count": 0
      }
    }
  }
]
```

### Criterion 5 — Bad Text Is Rejected And Not Decided

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "combined_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_c5_t1_1\"}",
    "audit_check": {
      "creator_id": "eval_c5_t1_1",
      "decision_entries": 0,
      "rejection_entries": 1,
      "entries": [
        {
          "creator_id": "eval_c5_t1_1",
          "error": "invalid_text",
          "event": "rejected",
          "http_status": 400,
          "reason": "invalid_text",
          "status": "rejected",
          "timestamp": "2026-11-11T19:24:57+00:00"
        }
      ]
    }
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "combined_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_c5_t1_2\"}",
    "audit_check": {
      "creator_id": "eval_c5_t1_2",
      "decision_entries": 0,
      "rejection_entries": 1,
      "entries": [
        {
          "creator_id": "eval_c5_t1_2",
          "error": "invalid_text",
          "event": "rejected",
          "http_status": 400,
          "reason": "invalid_text",
          "status": "rejected",
          "timestamp": "2026-11-11T19:24:57+00:00"
        }
      ]
    }
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "combined_score": null,
    "label": null,
    "sent": "(empty text)",
    "audit_check": {
      "creator_id": "eval_c5_t1_3",
      "decision_entries": 0,
      "rejection_entries": 1,
      "entries": [
        {
          "creator_id": "eval_c5_t1_3",
          "error": "invalid_text",
          "event": "rejected",
          "http_status": 400,
          "reason": "invalid_text",
          "status": "rejected",
          "timestamp": "2026-11-11T19:24:57+00:00"
        }
      ]
    }
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "combined_score": null,
    "label": null,
    "sent": "   ",
    "audit_check": {
      "creator_id": "eval_c5_t1_4",
      "decision_entries": 0,
      "rejection_entries": 1,
      "entries": [
        {
          "creator_id": "eval_c5_t1_4",
          "error": "invalid_text",
          "event": "rejected",
          "http_status": 400,
          "reason": "invalid_text",
          "status": "rejected",
          "timestamp": "2026-11-11T19:24:57+00:00"
        }
      ]
    }
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "combined_score": null,
    "label": null,
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "audit_check": {
      "creator_id": "eval_c5_t1_5",
      "decision_entries": 0,
      "rejection_entries": 1,
      "entries": [
        {
          "creator_id": "eval_c5_t1_5",
          "error": "text_too_long",
          "event": "rejected",
          "http_status": 413,
          "reason": "text_too_long",
          "status": "rejected",
          "timestamp": "2026-11-11T19:24:57+00:00"
        }
      ]
    }
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**Criterion 2 — MISSED on the approved substitute; original personal-writing
criterion remains unverified.** Across all three trials, the five AI-evasion
examples averaged 0.4317 while the five known-human examples averaged 0.6464,
so the gap was -0.2147 instead of the required +0.20. The main shared stage is
**signal one** (`detector.model_signal`): GPT-2 predictability does not track
authorship. Unusual wording and edits make generated prose less predictable,
while ordinary/formal human prose can be highly predictable. **Signal two**
also responds to text shape rather than meaning, and the **combining rule**
averages these imperfect signals (or returns 0.5 for strong disagreement).
This inverted gap is consistent with the false positives and evasions below;
it is not evidence about my own writing because I had no personal samples.

**Broken attacks — stages and mechanisms**

- **EV01 (signal one; combining rule):** The misspellings increase model
  surprise, leaving `model_score` at 0.1635. `style_score` 0.4334 does not
  counter it, so the weighted combined score is 0.231 and the attack receives
  the high-confidence-human label.
- **EV02 (signal two; combining rule):** Breaking prose into short sentences
  distorts sentence-length statistics (`style_score` 0.1172). Its difference
  from `model_score` 0.5943 exceeds the disagreement limit, so the combiner
  forces 0.5/unsure instead of an AI label.
- **EV03 (signal two; combining rule):** The pasted quotation changes the
  measured style (`style_score` 0.2852). The signals differ by less than the
  disagreement cutoff, so averaging yields 0.571/unsure, not AI.
- **EV04 (signal one; combining rule):** Unusual vocabulary raises
  perplexity and leaves `model_score` at 0.6114, below the AI threshold.
  Combined with style 0.4122 the result is 0.5616/unsure.
- **EV05 (signals one and two; combining rule):** Heavy human editing changes
  both predictability and surface shape; the scores fall to 0.3212 and 0.2168.
  Their weighted result is 0.2951, labeled human.
- **EV06 (signal two; combining rule):** One very long and one very short
  sentence create a shape the style heuristic reads as less AI-like
  (`style_score` 0.2507). The weighted score is 0.4922/unsure.
- **EV07 (signal two; combining rule):** Punctuation padding changes the
  punctuation/shape features; `style_score` falls to 0.3512. The combination
  is 0.5275/unsure.
- **EV08 (signal one; signal two; combining rule):** The below-window sample
  receives a low `model_score` of 0.2452, while the short-text style fallback
  is neutral at 0.5. The combined score remains below the human threshold,
  yielding a human label.
- **EV09 (signal two; combining rule):** A human opening paragraph moves the
  style score down to 0.2683 while the model score is 0.7042. Their difference
  exceeds the disagreement limit, forcing 0.5/unsure rather than AI.
- **FP02 (signal one; combining rule):** Formal human prose is highly
  predictable to the model (`model_score` 0.7387); style is also slightly
  AI-leaning at 0.5325. The combiner produces 0.6871 and the label mapping
  correctly applies the AI threshold. The failure is the evidence, not the
  threshold mapping.
- **FP03 (signal one; combining rule):** Carefully written second-language
  prose scores 0.8051 on model predictability and 0.5082 on style. The
  combined 0.7309 crosses the AI threshold and falsely labels a human sample.
- **FP05 (signal one; combining rule):** Human technical documentation is
  predictable (`model_score` 0.8005) and regular in shape (`style_score`
  0.5663). The weighted result 0.7419 maps to AI.
- **MF03, MF04, MF05, MF06, and MF07 (route validation):** The route checks
  that `text` is a nonempty string and within the character limit, but does
  not reject control characters, punctuation-only text, a single long token,
  emoji-only text, or right-to-left text. All five therefore reach scoring
  and become ordinary `decided` entries (unsure in this run), instead of
  being rejected as unusable input. The root stage is route validation; the
  model/style scores are not meaningful evidence of authorship for these
  malformed cases.

**Pattern:** Nine of ten evasion attacks succeeded by making signal one or
signal two produce a non-AI result, often with the combiner returning unsure
when the signals disagree. The three false positives show the inverse problem:
predictable human registers push signal one high, and neither the style score
nor the combiner reliably protects them. Five malformed inputs expose a
separate route-validation gap. The label mapping itself behaved consistently
in the label-coverage trial; changing its thresholds alone would trade one
error type for the other rather than fix the signal limitations.

Criteria 3, 4, and 5 were MET in every trial: all labels appeared, the appeal
workflow recorded one valid appeal and rejected an unknown ID without logging
an appeal, and every tested invalid text was rejected and logged without a
decision.


---

## The Improvement

**What I changed:** One change only: raised `AI_THRESHOLD` from `0.65` to
`0.75` in `config.py`. No signal weights, route behavior, or scenarios changed.

**Which diagnosis pointed at it:** The three false-positive attack examples
FP02, FP03, and FP05 had combined scores `0.6871`, `0.7309`, and `0.7419`.
Each was above the old threshold and below `0.75`, so the diagnosis pointed to
the label-mapping threshold as a targeted way to stop these high-confidence AI
labels without changing the model or style scores.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Ran the same 56 inputs with the same scenarios. Each result set is preserved:
[before attack report](./results/attack_run_2026-11-04_1819_before.md) and
[after attack report](./results/attack_run_2026-11-11_1333_after.md).

| Family | Before BROKE / HELD | After BROKE / HELD |
|---|---:|---:|
| Evasion | 9 / 1 | 9 / 1 |
| False positive | 3 / 5 | 0 / 8 |
| Flood (same creator) | 0 / 12 | 0 / 12 |
| Malformed | 5 / 15 | 5 / 15 |
| Prompt injection | 0 / 6 | 0 / 6 |
| **Total** | **17 / 39** | **14 / 42** |

FP02, FP03, and FP05 moved from `ai` to `unsure`; the underlying scores did
not change. EV01–EV09 still do not receive the high-confidence AI label, and
MF03–MF07 are still accepted and scored.

The three-trial evaluation is also recorded in the
[before report](./results/run_2026-11-11_1124_before.md) and
[after report](./results/run_2026-11-11_1333_after.md):

| Criterion | Before | After | Change |
|---|---:|---:|---|
| 1. My own writing flagged as AI | UNMEASURED | UNMEASURED | No personal samples available |
| 2. Score separation (approved substitute) | -0.2147 in all trials | -0.2147 in all trials | No change; still MISSED |
| 3. All three labels reachable | 3/3 in all trials | 2/3 in all trials | MISSED after threshold increase |
| 4. Appeal lifecycle | Pass in all trials | Pass in all trials | No change |
| 5. Invalid text rejected, not decided, and logged | 5/5 in all trials | 5/5 in all trials | No change |

**After-run output excerpts — Trial 1**, recorded by `run_attacks.py::main`
and `run_eval.py::main` (the complete per-input data is in the linked reports):

```json
{
  "id": "FP03",
  "status": 200,
  "guess": "unsure",
  "confidence": 0.4618,
  "model_score": 0.8051,
  "style_score": 0.5082,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "verdict": "HELD"
}
```

```json
[
  {
    "guess": "human",
    "combined_score": 0.231,
    "label": "We think this was probably written by a person."
  },
  {
    "guess": "unsure",
    "combined_score": 0.5721,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation."
  },
  {
    "guess": "unsure",
    "combined_score": 0.6871,
    "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation."
  }
]
```

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, narrowly: the attack-set false-positive labels fell from 3 to 0, and total
broken outcomes fell from 17 to 14. It did not improve score separation or
evasion resistance. The fixed label-coverage scenario used EV01, FP01, and
FP02; FP02's score `0.6871` is now unsure, so that scenario reaches only human
and unsure, not all three labels. This is the cost of the threshold change:
fewer false accusations in these examples, but fewer high-confidence AI
decisions and a missed label-coverage criterion.

---

## What's Still Broken

**Successful evasions (BROKE):** Each of these inputs still avoids a high-confidence AI label. I would improve the signal(s) or validate the input rather than lower the threshold again; I stopped because this iteration was limited to the one threshold change.

- **EV01 — signal one / combining rule:** Misspellings lower model predictability, producing a human label. I would test a signal less sensitive to spelling noise; I stopped before changing either signal.
- **EV02 — signal two / combining rule:** Short, broken-up sentences distort style statistics and the signal disagreement sends the result to unsure. I would make the style signal and disagreement rule more robust to sentence splitting; I stopped to keep the threshold as the only change.
- **EV03 — signal two / combining rule:** A pasted quotation shifts measured style and the combination remains unsure. I would evaluate quoted and non-quoted spans separately; I stopped because that changes signal behavior.
- **EV04 — signal one / combining rule:** Unusual vocabulary raises perplexity and keeps the combined score below the AI band. I would test whether the detector can distinguish rare vocabulary from authorship; I stopped rather than retune the model signal and threshold together.
- **EV05 — both signals / combining rule:** Heavy human editing changes predictability and surface shape enough to produce a human label. I would test the signals on edited AI text and redesign the combination if needed; I stopped to preserve a one-change comparison.
- **EV06 — signal two / combining rule:** One long and one short sentence distort the style features, leaving the result unsure. I would make the style features less sensitive to sentence-length extremes; I stopped before changing signal two.
- **EV07 — signal two / combining rule:** Punctuation padding changes the measured style and keeps the score out of the AI band. I would normalize or constrain punctuation features; I stopped before making a second behavior change.
- **EV08 — signal one, signal two / combining rule:** Text below the model's useful token window receives a low model score and a neutral short-text style fallback, yielding a human label. I would reject or specially handle text too short for reliable scoring; I stopped to avoid adding route validation to the threshold experiment.
- **EV09 — signal two / combining rule:** A human opening paragraph pulls style down, and disagreement forces unsure. I would test a chunk-aware approach rather than letting an opening dominate the whole text; I stopped because that requires a signal change.

**Malformed inputs still accepted and scored (BROKE):** The route checks basic type, non-whitespace content, and maximum length, but these cases still reach the signals. I would add targeted route validation for unusable text; I stopped because route validation would be a separate change from the threshold experiment.

- **MF03:** Control characters are accepted. I would reject or normalize disallowed control characters.
- **MF04:** Punctuation-only text is accepted. I would require meaningful text content.
- **MF05:** A very long single word is accepted. I would require a minimum amount of tokenized word content.
- **MF06:** Emoji-only text is accepted. I would require text content suitable for the detector.
- **MF07:** Right-to-left text is accepted without language/script-aware handling. I would add a deliberate multilingual validation and scoring policy rather than reject a script by default.

**Criteria still missed or unmeasured:**

- **Criterion 1 — UNMEASURED:** I would run the test with ten pieces of my own writing. I stopped because no user-authored samples were available; substituting somebody else's writing would not answer the criterion.
- **Criterion 2 — MISSED on the approved attack-set substitute:** The AI-evasion mean was `0.4317` and the known-human mean was `0.6464`, a gap of `-0.2147` instead of the required `+0.20`. I would improve and re-evaluate the signals on both groups; I stopped because changing signals as well as the threshold would make this before/after result hard to attribute.
- **Criterion 3 — MISSED:** The unchanged coverage scenario reaches human and unsure, but not AI, because its highest score is `0.6871` and the threshold is now `0.75`. I would add a stable, known-AI fixture that exercises the AI label (the after attack report includes EV10 at `0.845`) without lowering the threshold. I left the scenario unchanged so the before/after comparison stayed controlled.

Criteria 4 and 5 met their targets in all three trials. The 14 remaining BROKE outcomes are the nine evasions and five malformed-text cases listed above; the after-run attack report records all 56 individual outcomes.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I would favor fewer wrong accusations and keep the `0.75` threshold rather than label these human examples as AI. Writers whose genuine work might otherwise be falsely accused benefit, while reviewers, instructors, and readers bear the cost when AI-generated text below the threshold is not identified with a decisive AI label.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

**Fork repository URL:** https://github.com/aphan135/ai201-project4-provenance-guard-starter-v2026

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
