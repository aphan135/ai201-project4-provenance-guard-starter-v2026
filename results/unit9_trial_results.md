# Unit 9 — Three evaluation trials

The same five criteria and test cases were run three times, with no changes
between trials. Each trial used a fresh temporary JSONL audit file and sent
requests over HTTP to the local Flask service on loopback. Deterministic local
stubs returned fixed detector and stylometry scores; no external model or API
was called. This isolates route, trace, rejection, privacy, and persistence
behavior, but does not measure real model behavior.

The evaluator is [`run_unit9_eval.py`](../run_unit9_eval.py). Complete responses,
trace records, failure records, and per-case check results are saved in
[`unit9_trial_1.json`](./unit9_trial_1.json),
[`unit9_trial_2.json`](./unit9_trial_2.json), and
[`unit9_trial_3.json`](./unit9_trial_3.json).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Complete run trace for successful submissions | 10 of 10 HTTP 200 submissions have exactly one complete trace | 10/10 | 10/10 | 10/10 | MET |
| 2. Trace output matches caller response | 10 of 10 traces equal the full response and have a matching decision | 10/10 | 10/10 | 10/10 | MET |
| 3. Failed submissions leave matching traces | All 6 cases have expected status, one matching trace, no decision; first 5 have one rejection | 6/6 | 6/6 | 6/6 | MET |
| 4. Run traces do not expose submitted text | 10 of 10 sentinels absent; length and SHA-256 match | 10/10 | 10/10 | 10/10 | MET |
| 5. Run trace survives service restart | 1 of 1 successful submission is returned by `/log` after restart | 1/1 | 1/1 | 1/1 | MET |

The traces below were emitted by `log_submit_run()` in
[`app.py`](../app.py), written by `log_run()` in
[`audit.py`](../audit.py), and are copied from trial 1's saved JSON.

## Criterion 1 — Complete success trace

Ten distinct successful requests were checked in each trial. The following
actual run record contains the required timestamp, route, HTTP status,
duration, detector model, input summary, and output:

```json
{"timestamp":"2026-11-16T20:49:29.494+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c1_00","text_present":true,"text_type":"str","text_length":33,"text_sha256":"8bec5e27e94a29533972525d6d167cdb5b46a55e9c517340e4fe2079354cded8"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"e51f0ab0-b55c-47cc-92f8-8e7ce0e6b2a9","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":1.422,"http_status":200,"detector_model":"gpt2"}
```

Produced for the response by `submit()` and `log_submit_run()` in
[`app.py`](../app.py); persisted by `log_run()` in
[`audit.py`](../audit.py).

## Criterion 2 — Caller response matches trace and decision

The evaluator compared each returned JSON object with its run trace and found
one `decided` record with the same `content_id` for each of ten submissions in
each trial. Example actual run and decision records:

Actual `POST /submit` response (HTTP 200):

```json
{"combined_score":0.225,"confidence":0.55,"content_id":"2bd52b40-9e12-4cfe-b538-e829e4764d50","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3}
```

```json
{"timestamp":"2026-11-16T20:49:29.505+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c2_00","text_present":true,"text_type":"str","text_length":27,"text_sha256":"17ed2abbfdc5a70e59985fc2db11c036508767ccebf684b894b0dbb09492645e"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"2bd52b40-9e12-4cfe-b538-e829e4764d50","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":0.231,"http_status":200,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.505+00:00","content_id":"2bd52b40-9e12-4cfe-b538-e829e4764d50","creator_id":"m5_t1_c2_00","guess":"human","model_score":0.2,"style_score":0.3,"combined_score":0.225,"label":"We think this was probably written by a person.","status":"decided"}
```

The response and decision are produced by `submit()` in
[`app.py`](../app.py); the records are written by `log_run()` and
`log_decision()` in [`audit.py`](../audit.py).

## Criterion 3 — Failure traces and responses

All six deliberately triggered cases produced their expected status, one
matching run trace, and no decision. The first five also produced one
`rejected` record. Below are the actual responses and trace/rejection records
from trial 1. For the unhandled exception, Flask returned an HTML 500 body;
the run record captures its content type and body length.

### Missing `text` — HTTP 400

```text
{"error":"invalid_text","message":"text must be a non-empty string."}
```
```json
{"timestamp":"2026-11-16T20:49:29.514+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_0","text_present":false,"text_type":"missing"},"output":{"error":"invalid_text","message":"text must be a non-empty string."},"duration_ms":0.214,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.514+00:00","creator_id":"m5_t1_c3_0","event":"rejected","status":"rejected","reason":"invalid_text","error":"invalid_text","http_status":400}
```

### Whitespace-only text — HTTP 400

```text
{"error":"invalid_text","message":"text must be a non-empty string."}
```
```json
{"timestamp":"2026-11-16T20:49:29.516+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_1","text_present":true,"text_type":"str","text_length":3,"text_sha256":"0aad7da77d2ed59c396c99a74e49f3a4524dcdbcb5163251b1433d640247aeb4"},"output":{"error":"invalid_text","message":"text must be a non-empty string."},"duration_ms":0.343,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.515+00:00","creator_id":"m5_t1_c3_1","event":"rejected","status":"rejected","reason":"invalid_text","error":"invalid_text","http_status":400}
```

### Punctuation-only text — HTTP 400

```text
{"error":"punctuation_only_text","message":"text must contain something other than punctuation or whitespace."}
```
```json
{"timestamp":"2026-11-16T20:49:29.517+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_2","text_present":true,"text_type":"str","text_length":7,"text_sha256":"4d85f060696fdd4125bfc0f6508f6fb05be68bc859e5e24d48da0167ae603d2a"},"output":{"error":"punctuation_only_text","message":"text must contain something other than punctuation or whitespace."},"duration_ms":0.224,"http_status":400,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.517+00:00","creator_id":"m5_t1_c3_2","event":"rejected","status":"rejected","reason":"punctuation_only_text","error":"punctuation_only_text","http_status":400}
```

### 20,001-character text — HTTP 413

```text
{"error":"text_too_long","message":"text must not exceed 20000 characters."}
```
```json
{"timestamp":"2026-11-16T20:49:29.518+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_3","text_present":true,"text_type":"str","text_length":20001,"text_sha256":"991b716ebf8586a3b931be8ad3dd6d0979eb1049e05eeb714dbedbb06696ee3f"},"output":{"error":"text_too_long","message":"text must not exceed 20000 characters."},"duration_ms":0.275,"http_status":413,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.518+00:00","creator_id":"m5_t1_c3_3","event":"rejected","status":"rejected","reason":"text_too_long","error":"text_too_long","http_status":413}
```

### Detector unavailable — HTTP 503

```text
{"error":"detector_unavailable","message":"detector unavailable for test"}
```
```json
{"timestamp":"2026-11-16T20:49:29.519+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_4","text_present":true,"text_type":"str","text_length":22,"text_sha256":"9f19715933e4b8529e4619a91b7effb466b51e6455f31e9fb43384e301e2ef7e"},"output":{"error":"detector_unavailable","message":"detector unavailable for test"},"duration_ms":0.259,"http_status":503,"detector_model":"gpt2"}
{"timestamp":"2026-11-16T20:49:29.519+00:00","creator_id":"m5_t1_c3_4","event":"rejected","status":"rejected","reason":"detector_unavailable","error":"detector_unavailable","http_status":503}
```

### Unhandled runtime error — HTTP 500

Actual response body:

```html
<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

Actual run record; this case has no `rejected` record:

```json
{"timestamp":"2026-11-16T20:49:29.522+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c3_5","text_present":true,"text_type":"str","text_length":24,"text_sha256":"e5b8fa6e595b81f6d9c4068549a59a22a3c0fb822f686a37aad7635351359b24"},"output":{"content_type":"text/html; charset=utf-8","body_chars":265},"duration_ms":2.485,"http_status":500,"detector_model":"gpt2"}
```

The error cases exercise `submit()` and its request hooks in
[`app.py`](../app.py). The five handled errors call the route's `reject()`
helper, which writes `log_rejection()` in [`audit.py`](../audit.py); the
unhandled 500 is traced by `log_submit_run()` and `log_run()`.

## Criterion 4 — Submitted text is not in run traces

Ten distinct synthetic sentinel phrases were submitted in each trial. All
10/10 matching records in every trial omitted the literal phrase and retained
the correct character count and SHA-256 digest. The evaluator saves each
per-item check and digest in the trial JSON. Example actual record:

```json
{"timestamp":"2026-11-16T20:49:29.524+00:00","event":"run","route":"/submit","input":{"creator_id":"m5_t1_c4_00","text_present":true,"text_type":"str","text_length":40,"text_sha256":"cf87afde1b6ab97a617abaa40698a07ca53396f6010b91a0798d8fd7fda217d7"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"dcb17370-a316-4119-9fdd-4ded6811c37c","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"duration_ms":0.3,"http_status":200,"detector_model":"gpt2"}
```

This is the `/submit` trace produced by `log_submit_run()` in
[`app.py`](../app.py) and `log_run()` in [`audit.py`](../audit.py).

## Criterion 5 — Persistence across restart

The service accepted a submission, was stopped, and was started again using
the same audit file. The restarted `GET /log?limit=2` returned the matching
run record with the same `content_id` as the original response:

```text
POST /submit HTTP 200:
{"combined_score":0.225,"confidence":0.55,"content_id":"76eebf84-50b3-45e8-b819-40136cdbd5a9","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3}
```
```json
{"detector_model":"gpt2","duration_ms":0.858,"event":"run","http_status":200,"input":{"creator_id":"m5_t1_restart","text_length":64,"text_present":true,"text_sha256":"fc3d5e6ee2b6ecb3a46232c58ed6bf8b586939cada5cd1c77d3d67dd366f53d4","text_type":"str"},"output":{"combined_score":0.225,"confidence":0.55,"content_id":"76eebf84-50b3-45e8-b819-40136cdbd5a9","guess":"human","label":"We think this was probably written by a person.","model_score":0.2,"style_score":0.3},"route":"/submit","timestamp":"2026-11-16T20:49:29.752+00:00"}
```

The persisted entry is returned by `get_log()` in
[`app.py`](../app.py) using `read_entries()` in [`audit.py`](../audit.py).
