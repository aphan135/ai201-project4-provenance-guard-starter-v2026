# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 18:19
- Manually marked BROKE: **17**
- Manually marked HELD: **39**

The runner leaves verdicts for human review because an evasion's success
depends on the target and the returned decision. The table below records the
manual verdicts after comparing each target with the service response.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `28c8cd50-4303-4def-bcb8-c7e990e2c060` | human | 0.538 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1d80bf6e-9f40-4c27-84e5-12ade0ba5f4f` | unsure | 0.000 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `d99e9392-cded-485a-9d0b-8f173001124e` | unsure | 0.142 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `891650a5-a33c-455d-9c29-af49d9246048` | unsure | 0.123 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e0090b32-df6b-4bfc-8f1e-04c69ea4a60b` | human | 0.410 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `9984ab31-ec76-4b9d-b0bf-90c86c7b7007` | unsure | 0.016 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c3492bb6-24e1-430a-9070-20dc9fddfb32` | unsure | 0.055 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `a39829e4-f080-467f-a16c-d586834fa848` | human | 0.382 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `fe6701e3-a3e8-4b5e-85f3-bdb6fbd01d0b` | unsure | 0.000 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `eea2706f-c34b-423c-9400-03b67af8d673` | ai | 0.845 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `8d97dc97-87ef-4f11-b316-8b0f275d3bda` | unsure | 0.144 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `1efe7444-da41-44a8-ac2f-b393cab1d862` | ai | 0.374 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `90963e37-afa7-4bf9-879a-b72d62e7cfa1` | ai | 0.462 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `a5055471-3e74-42e8-b8d3-54d882637526` | unsure | 0.000 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `624d329b-233c-49a0-9376-32d2e8fc28aa` | ai | 0.484 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `0b26118e-0e2b-41f8-a4a9-b52335c19898` | unsure | 0.000 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `34ab5694-2680-4f4a-95c4-9995e3a5b40e` | unsure | 0.000 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `f0f23097-0a91-4f24-b8f3-b8da75b939a9` | unsure | 0.267 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c07ede88-a0fa-45c3-bd08-90f3adb89de9` | unsure | 0.224 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `9d5829b0-72e1-4953-9e36-a0b3676222cd` | human | 0.642 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `42144cbb-26c4-4cca-a486-3abb03c580da` | unsure | 0.051 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c2d691aa-a251-4928-b4d3-67c44c8164fb` | unsure | 0.104 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `81cf4017-6356-4287-8be2-dccb86fb3205` | unsure | 0.000 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c0ab9cd9-c009-4f7f-90f2-968194ad53ce` | unsure | 0.059 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `ad25a0d1-52dd-48ea-9ced-607b88bdd1e3` | unsure | 0.000 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `b52439b8-0a34-4320-a46a-5be21cc98758` | unsure | 0.000 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `df6e84f0-ae46-4440-be44-952b129983dd` | unsure | 0.000 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `a0fbfff0-2fa6-44dd-9691-4d58908855eb` | unsure | 0.000 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `abccf77b-a607-4354-9a6d-8ec620c67f68` | unsure | 0.000 | BROKE |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `135256bc-4d5d-42d0-8bd6-944b0fb5c296` | unsure | 0.000 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a948e021-3dbc-4d41-b4f7-b437e6f27b64` | unsure | 0.000 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `af8eb1aa-274f-4988-b1af-70572ccfe639` | unsure | 0.000 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f8b95e46-3231-4804-96c8-205f20ed1cf8` | unsure | 0.000 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `caf22abf-44db-49a7-b09c-a07e9ed05546` | unsure | 0.000 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | BROKE | HELD |
|---|---|---|---|
| `evasion` | 10 | 9 | 1 |
| `false_positive` | 8 | 3 | 5 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 5 | 15 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "28c8cd50-4303-4def-bcb8-c7e990e2c060",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.538,
  "model_score": 0.1635,
  "style_score": 0.4334,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1d80bf6e-9f40-4c27-84e5-12ade0ba5f4f",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.5943,
  "style_score": 0.1172,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "d99e9392-cded-485a-9d0b-8f173001124e",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.142,
  "model_score": 0.6662,
  "style_score": 0.2852,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "891650a5-a33c-455d-9c29-af49d9246048",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.1232,
  "model_score": 0.6114,
  "style_score": 0.4122,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e0090b32-df6b-4bfc-8f1e-04c69ea4a60b",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4098,
  "model_score": 0.3212,
  "style_score": 0.2168,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "9984ab31-ec76-4b9d-b0bf-90c86c7b7007",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.0156,
  "model_score": 0.5727,
  "style_score": 0.2507,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c3492bb6-24e1-430a-9070-20dc9fddfb32",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.055,
  "model_score": 0.5862,
  "style_score": 0.3512,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "a39829e4-f080-467f-a16c-d586834fa848",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3822,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "fe6701e3-a3e8-4b5e-85f3-bdb6fbd01d0b",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.7042,
  "style_score": 0.2683,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "eea2706f-c34b-423c-9400-03b67af8d673",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8448,
  "model_score": 0.9792,
  "style_score": 0.7518,
  "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "8d97dc97-87ef-4f11-b316-8b0f275d3bda",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1442,
  "model_score": 0.6175,
  "style_score": 0.436,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "1efe7444-da41-44a8-ac2f-b393cab1d862",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.3742,
  "model_score": 0.7387,
  "style_score": 0.5325,
  "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "90963e37-afa7-4bf9-879a-b72d62e7cfa1",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.4618,
  "model_score": 0.8051,
  "style_score": 0.5082,
  "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "a5055471-3e74-42e8-b8d3-54d882637526",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8329,
  "style_score": 0.3676,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "624d329b-233c-49a0-9376-32d2e8fc28aa",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.4838,
  "model_score": 0.8005,
  "style_score": 0.5663,
  "label": "We think this was probably written by AI, but this estimate is not proof of authorship.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0b26118e-0e2b-41f8-a4a9-b52335c19898",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8814,
  "style_score": 0.3717,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "34ab5694-2680-4f4a-95c4-9995e3a5b40e",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.8816,
  "style_score": 0.3961,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "f0f23097-0a91-4f24-b8f3-b8da75b939a9",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.2666,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c07ede88-a0fa-45c3-bd08-90f3adb89de9",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.2238,
  "model_score": 0.4625,
  "style_score": 0.165,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "9d5829b0-72e1-4953-9e36-a0b3676222cd",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6416,
  "model_score": 0.2044,
  "style_score": 0.1037,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "42144cbb-26c4-4cca-a486-3abb03c580da",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.0512,
  "model_score": 0.5943,
  "style_score": 0.3194,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c2d691aa-a251-4928-b4d3-67c44c8164fb",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.1036,
  "model_score": 0.4998,
  "style_score": 0.2932,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "81cf4017-6356-4287-8be2-dccb86fb3205",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.6401,
  "style_score": 0.1865,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c0ab9cd9-c009-4f7f-90f2-968194ad53ce",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0586,
  "model_score": 0.5583,
  "style_score": 0.4422,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "ad25a0d1-52dd-48ea-9ced-607b88bdd1e3",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "b52439b8-0a34-4320-a46a-5be21cc98758",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "df6e84f0-ae46-4440-be44-952b129983dd",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "a0fbfff0-2fa6-44dd-9691-4d58908855eb",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "abccf77b-a607-4354-9a6d-8ec620c67f68",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "135256bc-4d5d-42d0-8bd6-944b0fb5c296",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "a948e021-3dbc-4d41-b4f7-b437e6f27b64",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "af8eb1aa-274f-4988-b1af-70572ccfe639",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "f8b95e46-3231-4804-96c8-205f20ed1cf8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "caf22abf-44db-49a7-b09c-a07e9ed05546",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
