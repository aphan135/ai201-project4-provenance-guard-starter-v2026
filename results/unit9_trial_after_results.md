# Unit 9 — Milestone 6 results (after tightening)

The original Milestone 5 criteria all passed in all three trials. I did not
change the service or the original criterion wording. The one weak target was
criterion 5: one restart per trial checks only one clean lifecycle. I tightened
the follow-up check to require the same successful run record to be returned
after **three consecutive stop/restart cycles in each trial**.

The improvement is in [`run_unit9_eval.py`](../run_unit9_eval.py):
`run_restart_check()` now starts and stops the local Flask service three times
after the successful submission, calling `GET /log?limit=2` after every
restart and comparing the record's `content_id` and status with the original
response. The other four criteria, inputs, and checks are unchanged. Each trial
uses a fresh JSONL file, loopback HTTP, and deterministic local signal stubs;
no external model or API is used.

| Criterion | After target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Complete run trace for successful submissions | 10 of 10 HTTP 200 submissions have exactly one complete trace | 10/10 | 10/10 | 10/10 | MET |
| 2. Trace output matches caller response | 10 of 10 traces equal the full response and have a matching decision | 10/10 | 10/10 | 10/10 | MET |
| 3. Failed submissions leave matching traces | All 6 cases have expected status, one matching trace, no decision; first 5 have one rejection | 6/6 | 6/6 | 6/6 | MET |
| 4. Run traces do not expose submitted text | 10 of 10 sentinels absent; length and SHA-256 match | 10/10 | 10/10 | 10/10 | MET |
| 5. Run trace survives repeated restarts | Same trace is returned after all 3 consecutive restarts | 3/3 | 3/3 | 3/3 | MET |

Full after-run evidence is saved in
[`unit9_trial_1.json`](./unit9_trial_1.json),
[`unit9_trial_2.json`](./unit9_trial_2.json), and
[`unit9_trial_3.json`](./unit9_trial_3.json). The original one-restart
baseline and its outputs remain in [`unit9_trial_results.md`](./unit9_trial_results.md),
[`unit9_trial_before_1.json`](./unit9_trial_before_1.json),
[`unit9_trial_before_2.json`](./unit9_trial_before_2.json), and
[`unit9_trial_before_3.json`](./unit9_trial_before_3.json).

## Criterion 1 — Successful request trace

Actual run record from trial 1:

```json
{"timestamp":"2026-11-16T20:57:11.952+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c1_00","text_present":true,"text_type":"str","text_length":33,"text_sha256":"8bec5e27e94a29533972525d6d167cdb5b46a55e9c517340e4fe2079354cded8"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"44d7afa6-bbf2-4d7c-ab9c-941cafd37959","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":2.479,"http_status":200,"detector_model":"gpt2"}
```

Produced by `submit()` and `log_submit_run()` in
[`app.py`](../app.py), written by `log_run()` in [`audit.py`](../audit.py).

## Criterion 2 — Response and audit output match

Actual HTTP response:

```json
{"combined_score":0.225,"confidence":0.55,"content_id":"12992f4f-2c4d-4733-8330-070b6e499a74","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3}
```

Matching run and decision records:

```json
{"timestamp":"2026-11-16T20:57:11.964+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c2_00","text_present":true,"text_type":"str","text_length":27,"text_sha256":"17ed2abbfdc5a70e59985fc2db11c036508767ccebf684b894b0dbb09492645e"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"12992f4f-2c4d-4733-8330-070b6e499a74","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":0.426,"http_status":200,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.963+00:00","content_id":"12992f4f-2c4d-4733-8330-070b6e499a74","creator_id":"m5_t1_c2_00","guess":"human","model_score":0.2,"style_score":0.3,"combined_score":0.225,"label":"We think this was probably written by a person.","status":"decided"}
```

The response and decision are from `submit()` in [`app.py`](../app.py);
the trace and decision are written by `log_run()` and `log_decision()` in
[`audit.py`](../audit.py).

## Criterion 3 — Failure responses and traces

The six actual trial-1 responses and their corresponding run/rejection records
follow. `submit()` and its request hooks in [`app.py`](../app.py) produce the
responses/traces; `log_rejection()` in [`audit.py`](../audit.py) writes the
five handled-rejection records. The unhandled 500 intentionally has no
`rejected` record.

### Missing `text` — HTTP 400

```text
{"error":"invalid_text","message":"text must be a non-empty string."}
```
```json
{"timestamp":"2026-11-16T20:57:11.974+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_0","text_present":false,"text_type":"missing"},"output":{"error":"invalid_text","message":"text must be a non-empty string."},"duration_ms":0.229,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.974+00:00","creator_id":"m5_t1_c3_0","event":"rejected","status":"rejected","reason":"invalid_text","error":"invalid_text","http_status":400}
```

### Whitespace-only text — HTTP 400

```text
{"error":"invalid_text","message":"text must be a non-empty string."}
```
```json
{"timestamp":"2026-11-16T20:57:11.975+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_1","text_present":true,"text_type":"str","text_length":3,"text_sha256":"0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4"},"output":{"error":"invalid_text","message":"text must be a non-empty string."},"duration_ms":0.233,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.975+00:00","creator_id":"m5_t1_c3_1","event":"rejected","status":"rejected","reason":"invalid_text","error":"invalid_text","http_status":400}
```

### Punctuation-only text — HTTP 400

```text
{"error":"punctuation_only_text","message":"text must contain something other than punctuation or whitespace."}
```
```json
{"timestamp":"2026-11-16T20:57:11.976+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_2","text_present":true,"text_type":"str","text_length":7,"text_sha256":"4d85f060696fdd4125bfc0f6508f6fb05be68bc859e5e24d48da0167ae603d2a"},"output":{"error":"punctuation_only_text","message":"text must contain something other than punctuation or whitespace."},"duration_ms":0.215,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.976+00:00","creator_id":"m5_t1_c3_2","event":"rejected","status":"rejected","reason":"punctuation_only_text","error":"punctuation_only_text","http_status":400}
```

### 20,001-character text — HTTP 413

```text
{"error":"text_too_long","message":"text must not exceed 20000 characters."}
```
```json
{"timestamp":"2026-11-16T20:57:11.977+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_3","text_present":true,"text_type":"str","text_length":20001,"text_sha256":"991b716ebf8586a3b931be8ad3dd6d0979eb1049e05eeb714dbedbb06696ee3f"},"output":{"error":"text_too_long","message":"text must not exceed 20000 characters."},"duration_ms":0.323,"http_status":413,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.977+00:00","creator_id":"m5_t1_c3_3","event":"rejected","status":"rejected","reason":"text_too_long","error":"text_too_long","http_status":413}
```

### Detector unavailable — HTTP 503

```text
{"error":"detector_unavailable","message":"detector unavailable for test"}
```
```json
{"timestamp":"2026-11-16T20:57:11.978+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_4","text_present":true,"text_type":"str","text_length":22,"text_sha256":"9f19715933e4b8529e4619a91b7effb466b51e6455f31e9fb43384e301e2ef7e"},"output":{"error":"detector_unavailable","message":"detector unavailable for test"},"duration_ms":0.235,"http_status":503,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:57:11.978+00:00","creator_id":"m5_t1_c3_4","event":"rejected","status":"rejected","reason":"detector_unavailable","error":"detector_unavailable","http_status":503}
```

### Unhandled runtime error — HTTP 500

Actual HTTP body:

```html
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

Actual run record:

```json
{"timestamp":"2026-11-16T20:57:11.981+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_5","text_present":true,"text_type":"str","text_length":24,"text_sha256":"e5b8fa6e595b81f6d9c4068549a59a22a3c0fb822f686a37aad7635351359b24"},"output":{"content_type":"text/html; charset=utf-8","body_chars":265},"duration_ms":2.06,"http_status":500,"detector_model":"gpt2"}
```

## Criterion 4 — Sentinel privacy

All 10 distinct sentinel inputs in each trial were absent from their matching
audit records, and each trace's length and SHA-256 matched the input. The
per-item results and digests are in the trial JSON. Example real record:

```json
{"timestamp":"2026-11-16T20:57:11.983+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c4_00","text_present":true,"text_type":"str","text_length":40,"text_sha256":"cf87afde1b6ab97a617abaa40698a07ca53396f6010b91a0798d8fd7fda217d7"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"c08822b3-9370-49dd-b500-61d0a7713605","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":0.27,"http_status":200,"detector_model":"gpt2"}
```

This trace is generated by `log_submit_run()` in [`app.py`](../app.py) and
`log_run()` in [`audit.py`](../audit.py).

## Criterion 5 — Same record survives three restarts

The successful submission returned this `content_id`:

```text
HTTP 200:
{"combined_score":0.225,"confidence":0.55,"content_id":"6578cd82-66bb-43b6-af3f-50dc0762edd4","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3}
```

Each of the three post-restart `GET /log?limit=2` responses returned HTTP 200
and this same run record with that `content_id`:

```json
{"detector_model":"gpt2","duration_ms":0.841,"event":"run","http_status":200,"input":{"creator_id":"m5_t1_restart","text_length":64,"text_present":true,"text_sha256":"fc3d5e6ee2b6ecb3a46232c58ed6bf8b586939cada5cd1c77d3d67dd366f53d4","text_type":"str"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"6578cd82-66bb-43b6-af3f-50dc0762edd4","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"route":"/submit","timestamp":"2026-11-16T20:57:12.210+00:00"}
```

The service returns persisted entries through `get_log()` in
[`app.py`](../app.py) and `read_entries()` in [`audit.py`](../audit.py).
