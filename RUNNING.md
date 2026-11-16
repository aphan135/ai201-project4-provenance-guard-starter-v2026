# Running Provenance Guard

## Run path: local with logs

Provenance Guard runs on the same machine as its local GPT-2 model. It does
not call a hosted API, so there is no hosted URL or API key. Flask binds to
`127.0.0.1:5000` by default, and the request trace and audit events append to
`logs/audit.jsonl`.

## Clone and prepare

Clone the repository into a new folder, then create an environment with a
supported Python version:

```bash
git clone https://github.com/aphan135/ai201-project4-provenance-guard-starter-v2026.git provenance-guard
cd provenance-guard
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test.py
```

Python 3.11, 3.12, and 3.13 are supported; Python 3.13 is the recommended
version. On Windows, create the environment with `py -3.13 -m venv .venv`
and activate it with `.venv\Scripts\Activate.ps1`.

The first submission downloads the model if it is not cached yet. To do that
before starting the service, run:

```bash
python detector.py
```

This downloads roughly 550 MB. No credentials are required.

## Start and verify

In the activated environment, start the local service:

```bash
AI201_DEBUG=0 python app.py
```

On PowerShell, use `$env:AI201_DEBUG="0"; python app.py`. The service prints
its address and model. Keep this terminal open.

In a second terminal, check the control route:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

Then submit text and inspect the response:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "A sufficiently long sample of ordinary writing goes here.", "creator_id": "local-check-1"}'
```

The first `/submit` may take longer while the model loads. A successful
response includes a `content_id`, both signal scores, the combined score, and
the label. To read the most recent records:

```bash
curl "http://127.0.0.1:5000/log?limit=10"
```

On PowerShell, use `curl.exe` and put each command on one line.

## What gets logged

`logs/audit.jsonl` is append-only JSON Lines. Each `/submit` request adds a
`run` record with a UTC timestamp, route, input summary, response output,
HTTP status, detector model, and `duration_ms`. The input summary keeps the
creator ID and the text's character count and SHA-256 digest; it deliberately
does not store submitted text verbatim. Successful decisions and rejected
requests also retain their existing domain-specific audit records.

Handled errors (including rejected input, unavailable detector, and rate
limits) are recorded with their response. An unhandled exception gets a
500 run record from the request teardown hook, including its exception type.
The response body is not copied into the log for non-JSON server errors.

## Test commands

Run the focused endpoint tests:

```bash
python -m unittest -v test_submission
```

Run the environment and `/ping` check:

```bash
python test.py
```

`test.py` checks the Python version, installed packages, model cache, and that
`/ping` responds. The focused tests use mocked scoring signals and do not
download the model.

## Local settings

| Setting | Default | Purpose |
|---|---|---|
| `HOST` | `127.0.0.1` | Local-only bind address |
| `PORT` | `5000` | HTTP port |
| `AI201_DEBUG` | `1` | Flask debug mode; keep disabled when testing runs |
| `AI201_DETECTOR_MODEL` | `gpt2` | Hugging Face model used by the local detector |

Rate limiting is enabled at five submissions per minute and 100 per day per
creator. Use a distinct `creator_id` for each of ten measurement requests so
the per-minute cap does not distort the timing sample.

## Troubleshooting

| Symptom | Check |
|---|---|
| `python test.py` reports Python 3.14 | Create a fresh environment with Python 3.11–3.13; 3.14 is outside the tested range |
| `Address already in use` | Another service is using port 5000; stop it or set a different `PORT` |
| First submission is slow | The local model is loading; later requests reuse it in the same process |
| `detector_unavailable` | Check network access for the initial model download, then run `python detector.py` |
| `429 rate_limited` | Wait for the per-minute window or use a distinct creator ID for an independent test |
| A run returns `500` | Check the `run` record in `logs/audit.jsonl`; it includes status, duration, and the exception type for unhandled failures |
