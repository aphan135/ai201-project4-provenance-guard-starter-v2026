# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 13:33
- Manually marked BROKE: **14**
- Manually marked HELD: **42**

Verdicts are based on each attack's stated target and the returned response.
The full table below records each manual HELD or BROKE judgment.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2e964a35-6eaf-4e3f-9729-04b33c43c1bb` | human | 0.538 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `20b1ee7e-1a4a-4bda-8514-03e156b7964a` | unsure | 0.000 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `acaa8172-5726-4195-851e-94dfcce7e86a` | unsure | 0.142 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cd1a2935-2ce2-41b3-ba0b-d5110872f3fc` | unsure | 0.123 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6fa0cf1f-4318-422a-b3bb-585dd0f568cb` | human | 0.410 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `501a530f-1d8d-417f-b937-08a99330899f` | unsure | 0.016 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a8d7271d-64a0-463d-87b0-fd69486d7239` | unsure | 0.055 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `163af59d-c732-49b2-8c61-6097e12c011f` | human | 0.382 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6e5e2df8-eb6b-4d59-a534-d80b123b54a0` | unsure | 0.000 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `33a17d47-36b4-470d-807a-e2d25a6952d3` | ai | 0.845 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d41b7b6b-10bd-42e0-bcc7-3d3dfb3f40c4` | unsure | 0.144 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `789bc94e-113f-4dc6-909a-be9d071bd81a` | unsure | 0.374 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b81a477d-1413-4359-be77-02d401fd49a4` | unsure | 0.462 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `44786798-7910-442a-8189-71857bc336a0` | unsure | 0.000 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `9f973b3c-6c2d-4f59-99d3-aa2274b20576` | unsure | 0.484 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `93c58dc0-589f-4262-9446-9276d5be6fe6` | unsure | 0.000 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `29bb065f-54b0-410a-822c-7f58c958753c` | unsure | 0.000 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `51495047-c1b7-4cf0-bc5e-602018ffaded` | unsure | 0.267 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `885d72e5-5e99-4e71-8c2b-ee32ba53feea` | unsure | 0.224 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c2623cbe-b4ee-4770-85be-74cbc7c6751c` | human | 0.642 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1d7e5dd3-0df1-48c2-a132-5281582431f2` | unsure | 0.051 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `49cb419a-7635-4f9b-8431-004f73250a2a` | unsure | 0.104 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ed3005f7-ee57-4a07-be8f-7218e1760021` | unsure | 0.000 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `635b068f-ab9b-4aa0-a79d-43009a176fee` | unsure | 0.059 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `7297737e-0dc6-44dc-b057-5a40479ba44b` | unsure | 0.000 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `8cff4aa8-36b5-4fd5-894a-fe045cfcfbb2` | unsure | 0.000 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `673a700a-7af8-493b-8981-498709b12b8c` | unsure | 0.000 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `b4ff7e3f-eefd-4ccf-bc26-8211d02e7410` | unsure | 0.000 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `fb7719f1-f970-403d-84ab-2d6accb7bb22` | unsure | 0.000 | BROKE |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `202f35ef-9392-4ef6-9c7a-4e550a7bba41` | unsure | 0.000 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aa53b6e5-b77d-4935-b94e-0a1d7c3ae366` | unsure | 0.000 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `82f523f6-8599-4738-a1cd-0d6865abf8ab` | unsure | 0.000 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `59a445b5-a875-4cae-ada8-239b61ab771e` | unsure | 0.000 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2525ffdf-128f-479c-96a9-fb0dd437a04c` | unsure | 0.000 | HELD |
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
| `false_positive` | 8 | 0 | 8 |
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
  "content_id": "2e964a35-6eaf-4e3f-9729-04b33c43c1bb",
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
  "content_id": "20b1ee7e-1a4a-4bda-8514-03e156b7964a",
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
  "content_id": "acaa8172-5726-4195-851e-94dfcce7e86a",
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
  "content_id": "cd1a2935-2ce2-41b3-ba0b-d5110872f3fc",
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
  "content_id": "6fa0cf1f-4318-422a-b3bb-585dd0f568cb",
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
  "content_id": "501a530f-1d8d-417f-b937-08a99330899f",
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
  "content_id": "a8d7271d-64a0-463d-87b0-fd69486d7239",
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
  "content_id": "163af59d-c732-49b2-8c61-6097e12c011f",
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
  "content_id": "6e5e2df8-eb6b-4d59-a534-d80b123b54a0",
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
  "content_id": "33a17d47-36b4-470d-807a-e2d25a6952d3",
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
  "content_id": "d41b7b6b-10bd-42e0-bcc7-3d3dfb3f40c4",
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
  "content_id": "789bc94e-113f-4dc6-909a-be9d071bd81a",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.3742,
  "model_score": 0.7387,
  "style_score": 0.5325,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "b81a477d-1413-4359-be77-02d401fd49a4",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.4618,
  "model_score": 0.8051,
  "style_score": 0.5082,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "44786798-7910-442a-8189-71857bc336a0",
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
  "content_id": "9f973b3c-6c2d-4f59-99d3-aa2274b20576",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.4838,
  "model_score": 0.8005,
  "style_score": 0.5663,
  "label": "We can't tell who wrote this from the text alone. If you wrote it, this result is not an accusation.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "93c58dc0-589f-4262-9446-9276d5be6fe6",
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
  "content_id": "29bb065f-54b0-410a-822c-7f58c958753c",
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
  "content_id": "51495047-c1b7-4cf0-bc5e-602018ffaded",
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
  "content_id": "885d72e5-5e99-4e71-8c2b-ee32ba53feea",
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
  "content_id": "c2623cbe-b4ee-4770-85be-74cbc7c6751c",
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
  "content_id": "1d7e5dd3-0df1-48c2-a132-5281582431f2",
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
  "content_id": "49cb419a-7635-4f9b-8431-004f73250a2a",
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
  "content_id": "ed3005f7-ee57-4a07-be8f-7218e1760021",
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
  "content_id": "635b068f-ab9b-4aa0-a79d-43009a176fee",
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
  "content_id": "7297737e-0dc6-44dc-b057-5a40479ba44b",
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
  "content_id": "8cff4aa8-36b5-4fd5-894a-fe045cfcfbb2",
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
  "content_id": "673a700a-7af8-493b-8981-498709b12b8c",
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
  "content_id": "b4ff7e3f-eefd-4ccf-bc26-8211d02e7410",
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
  "content_id": "fb7719f1-f970-403d-84ab-2d6accb7bb22",
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
  "content_id": "202f35ef-9392-4ef6-9c7a-4e550a7bba41",
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
  "content_id": "aa53b6e5-b77d-4935-b94e-0a1d7c3ae366",
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
  "content_id": "82f523f6-8599-4738-a1cd-0d6865abf8ab",
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
  "content_id": "59a445b5-a875-4cae-ada8-239b61ab771e",
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
  "content_id": "2525ffdf-128f-479c-96a9-fb0dd437a04c",
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
