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

The model score was `0.7335` and the style score was `0.5654`; their difference (`0.1681`) is below the `0.40` disagreement cutoff. The weighted result, `0.75 × 0.7335 + 0.25 × 0.5654 = 0.691475`, rounded to `0.6915`, with `confidence: 0.383`. That is above the `0.65` AI threshold, so the response labeled it **“We think this was probably written by AI, but this estimate is not proof of authorship.”** This is an observed false positive on this human-authored chat text, not evidence that the detector will flag every writer or genre.

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

**The numbers:** `0.75 × model_score + 0.25 × style_score`; disagreement cutoff `0.40`; human threshold `0.35`; AI threshold `0.65`. The current `confidence` is `2 × |combined_score − 0.50|`; it expresses distance from uncertainty, not a calibrated probability.

**Why these numbers:** The detector score is the more direct signal, so it gets three quarters of the weight. The text-only style heuristic is comparatively easy to shift through editing or genre, so it gets one quarter. A disagreement of 0.40 is large enough that averaging could hide material conflict; sending that case to the midpoint avoids a high-confidence claim. The wide `0.35`–`0.65` unsure band also favors avoiding false accusations.

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
| unsure | above `0.35` and below `0.65` | “We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.” |
| high-confidence AI | `0.65–1.00` inclusive | “We think this was probably written by AI, but this estimate is not proof of authorship.” |

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

---

## How I Used AI

**Moment 1**

- *What I asked for:* Trace the starter's submission flow, identify what the detector and planned style signal can and cannot tell, and specify both endpoint contracts before implementing them.
- *What came back:* A seven-step intended request path, signal blind spots, false-positive scenario, and proposed request/response fields. The initial explanation treated the desired flow as if it were already implemented.
- *What I changed:* I checked the actual route and audit helpers, then made the README distinguish planned behavior from runtime behavior. I also made the false-positive example explicitly hypothetical and recorded that labels and appeal were not working yet at that stage.

**Moment 2**

- *What I asked for:* Implement and test a second, text-only signal and combine it with the model signal, preserving both component scores in the response and audit log.
- *What came back:* Implementations for sentence-length spread, type-token ratio, punctuation density, a normalized style score, and a weighted combiner with a disagreement-to-uncertain rule; plus measured sample outputs.
- *What I changed:* I checked the standalone detector and stylometry outputs and the live endpoint/log results, documented the weights and blind spots, and kept the lightly edited AI false negative visible rather than tuning the threshold to hide it. I also noted that the combining rule was documented after its first implementation, not before.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
