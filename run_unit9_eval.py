#!/usr/bin/env python3
"""Run three repeatable trials for the Unit 9 instrumentation criteria."""

import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"

SERVICE_BOOTSTRAP = r"""
import os
import sys
import types
from pathlib import Path

import config
config.AUDIT_LOG = Path(os.environ["M5_AUDIT_LOG"])
config.LOG_DIR = config.AUDIT_LOG.parent

detector = types.ModuleType("detector")
class DetectorUnavailable(Exception):
    pass
detector.DetectorUnavailable = DetectorUnavailable
detector._model = None
def model_signal(text):
    if text == "M5_TRIGGER_UNAVAILABLE":
        raise DetectorUnavailable("detector unavailable for test")
    if text == "M5_TRIGGER_RUNTIME_ERROR":
        raise RuntimeError("model process failed for test")
    return 0.2
detector.model_signal = model_signal
sys.modules["detector"] = detector

stylometry = types.ModuleType("stylometry")
stylometry.style_signal = lambda text: 0.3
sys.modules["stylometry"] = stylometry

import app
app.app.run(
    host="127.0.0.1",
    port=int(os.environ["M5_PORT"]),
    debug=False,
    use_reloader=False,
)
"""


def http_json(url, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status, body = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, body = error.code, error.read()
    try:
        parsed = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = body.decode("utf-8", errors="replace")
    return status, parsed


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def start_service(log_path, port):
    environment = {
        **os.environ,
        "M5_AUDIT_LOG": str(log_path),
        "M5_PORT": str(port),
        "AI201_DEBUG": "0",
    }
    return subprocess.Popen(
        [sys.executable, "-c", SERVICE_BOOTSTRAP],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def stop_service(process):
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


def wait_for_service(process, base_url):
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Local service exited with status {process.returncode}")
        try:
            status, body = http_json(f"{base_url}/health")
            if status == 200 and isinstance(body, dict) and body.get("ok"):
                return
        except (OSError, ValueError):
            pass
        time.sleep(0.1)
    raise TimeoutError("Local service did not become ready within 20 seconds")


class LocalService:
    def __init__(self, log_path):
        self.port = free_port()
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.process = start_service(log_path, self.port)

    def __enter__(self):
        try:
            wait_for_service(self.process, self.base_url)
        except Exception:
            stop_service(self.process)
            raise
        return self.base_url

    def __exit__(self, exc_type, exc_value, traceback):
        stop_service(self.process)


def read_entries(audit_path):
    if not audit_path.exists():
        return []
    return [
        json.loads(line)
        for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def matching_run(entries, creator_id):
    return [
        entry for entry in entries
        if (
            entry.get("event") == "run"
            and entry.get("input", {}).get("creator_id") == creator_id
        )
    ]


def audit_records_for(entries, creator_id):
    return [
        entry for entry in entries
        if (
            entry.get("input", {}).get("creator_id") == creator_id
            or entry.get("creator_id") == creator_id
        )
    ]


def valid_run_trace(entry, creator_id):
    try:
        timestamp = datetime.fromisoformat(entry["timestamp"])
    except (KeyError, TypeError, ValueError):
        return False
    input_data = entry.get("input", {})
    return (
        entry.get("event") == "run"
        and entry.get("route") == "/submit"
        and entry.get("http_status") == 200
        and timestamp.utcoffset() == timedelta(0)
        and entry.get("duration_ms", -1) >= 0
        and bool(entry.get("detector_model"))
        and input_data.get("creator_id") == creator_id
        and isinstance(input_data.get("text_length"), int)
        and bool(re.fullmatch(r"[0-9a-f]{64}", input_data.get("text_sha256", "")))
        and isinstance(entry.get("output"), dict)
        and bool(entry["output"])
    )


def response_record(status, body):
    return {"status": status, "body": body}


def submit(base_url, payload):
    return http_json(f"{base_url}/submit", "POST", payload)


def run_restart_check(trial_number, log_path):
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    creator_id = f"m5_t{trial_number}_restart"
    payload = {
        "creator_id": creator_id,
        "text": "A short synthetic submission used to test persisted run records.",
    }

    first = start_service(log_path, port)
    try:
        wait_for_service(first, base_url)
        status, response = submit(base_url, payload)
    finally:
        stop_service(first)

    second = start_service(log_path, port)
    try:
        wait_for_service(second, base_url)
        read_status, log_response = http_json(f"{base_url}/log?limit=2")
    finally:
        stop_service(second)

    candidates = [
        entry for entry in log_response.get("entries", [])
        if (
            entry.get("event") == "run"
            and entry.get("input", {}).get("creator_id") == creator_id
        )
    ]
    run_entry = candidates[0] if candidates else None
    passed = (
        status == 200
        and isinstance(response, dict)
        and read_status == 200
        and run_entry is not None
        and run_entry.get("output", {}).get("content_id") == response.get("content_id")
        and run_entry.get("http_status") == 200
        and all(key in run_entry for key in ("timestamp", "input", "output", "duration_ms"))
    )
    return {
        "passed": passed,
        "submit_response": response_record(status, response),
        "log_response_status": read_status,
        "restarted_log_response": log_response,
        "matching_run": run_entry,
    }


def run_live_criteria(trial_number, audit_path):
    results = {"trial": trial_number, "criteria": {}}
    with LocalService(audit_path) as base_url:
        criterion_one_evidence = []
        criterion_one_checks = []
        for index in range(10):
            creator_id = f"m5_t{trial_number}_c1_{index:02}"
            text = f"Routine synthetic submission {trial_number}-{index}."
            status, body = submit(
                base_url,
                {"creator_id": creator_id, "text": text},
            )
            traces = matching_run(read_entries(audit_path), creator_id)
            passed = (
                status == 200
                and len(traces) == 1
                and valid_run_trace(traces[0], creator_id)
            )
            criterion_one_checks.append(passed)
            criterion_one_evidence.append({
                "response": response_record(status, body),
                "run": traces[0] if traces else None,
            })
        results["criteria"]["1"] = {
            "passed": sum(criterion_one_checks),
            "total": 10,
            "checks": criterion_one_checks,
            "evidence": criterion_one_evidence,
        }

        criterion_two_evidence = []
        criterion_two_checks = []
        for index in range(10):
            creator_id = f"m5_t{trial_number}_c2_{index:02}"
            status, body = submit(
                base_url,
                {
                    "creator_id": creator_id,
                    "text": f"Output matching sample {trial_number}-{index}.",
                },
            )
            entries = read_entries(audit_path)
            traces = matching_run(entries, creator_id)
            decisions = [
                entry for entry in entries
                if (
                    entry.get("status") == "decided"
                    and entry.get("content_id") == (body or {}).get("content_id")
                )
            ]
            passed = (
                status == 200
                and len(traces) == 1
                and traces[0].get("output") == body
                and len(decisions) == 1
            )
            criterion_two_checks.append(passed)
            criterion_two_evidence.append({
                "response": response_record(status, body),
                "run": traces[0] if traces else None,
                "decision": decisions[0] if decisions else None,
            })
        results["criteria"]["2"] = {
            "passed": sum(criterion_two_checks),
            "total": 10,
            "checks": criterion_two_checks,
            "evidence": criterion_two_evidence,
        }

        cases = [
            ("missing_text", {}, 400),
            ("whitespace", {"text": "   "}, 400),
            ("punctuation", {"text": "!!! ..."}, 400),
            ("oversized", {"text": "x" * 20_001}, 413),
            ("detector_unavailable", {"text": "M5_TRIGGER_UNAVAILABLE"}, 503),
            ("runtime_error", {"text": "M5_TRIGGER_RUNTIME_ERROR"}, 500),
        ]
        criterion_three_evidence = []
        criterion_three_checks = []
        for index, (case_name, partial_payload, expected_status) in enumerate(cases):
            creator_id = f"m5_t{trial_number}_c3_{index}"
            payload = {"creator_id": creator_id, **partial_payload}
            status, body = submit(base_url, payload)
            entries = read_entries(audit_path)
            traces = matching_run(entries, creator_id)
            rejections = [
                entry for entry in entries
                if entry.get("event") == "rejected" and entry.get("creator_id") == creator_id
            ]
            decisions = [
                entry for entry in entries
                if entry.get("status") == "decided" and entry.get("creator_id") == creator_id
            ]
            trace = traces[0] if len(traces) == 1 else None
            output_matches = (
                trace is not None
                and (
                    trace.get("output") == body
                    if expected_status != 500
                    else (
                        "content_type" in trace.get("output", {})
                        and trace["output"].get("body_chars", 0) > 0
                    )
                )
            )
            passed = (
                status == expected_status
                and trace is not None
                and trace.get("http_status") == expected_status
                and output_matches
                and not decisions
                and len(rejections) == (0 if expected_status == 500 else 1)
            )
            criterion_three_checks.append(passed)
            criterion_three_evidence.append({
                "case": case_name,
                "expected_status": expected_status,
                "response": response_record(status, body),
                "run": trace,
                "rejection": rejections[0] if rejections else None,
                "decision_count": len(decisions),
            })
        results["criteria"]["3"] = {
            "passed": sum(criterion_three_checks),
            "total": 6,
            "checks": criterion_three_checks,
            "evidence": criterion_three_evidence,
        }

        criterion_four_checks = []
        criterion_four_evidence = []
        for index in range(10):
            creator_id = f"m5_t{trial_number}_c4_{index:02}"
            sentinel = f"PrivateSyntheticSentinel trial-{trial_number} item-{index:02}"
            status, _ = submit(
                base_url,
                {"creator_id": creator_id, "text": sentinel},
            )
            entries = read_entries(audit_path)
            records = audit_records_for(entries, creator_id)
            traces = matching_run(entries, creator_id)
            digest = hashlib.sha256(sentinel.encode("utf-8")).hexdigest()
            leaked = any(sentinel in json.dumps(entry, ensure_ascii=False) for entry in records)
            passed = (
                status == 200
                and len(traces) == 1
                and not leaked
                and traces[0].get("input", {}).get("text_length") == len(sentinel)
                and traces[0].get("input", {}).get("text_sha256") == digest
            )
            criterion_four_checks.append(passed)
            criterion_four_evidence.append({
                "passed": passed,
                "creator_id": creator_id,
                "text_length": len(sentinel),
                "text_sha256": digest,
                "leaked": leaked,
                "run": traces[0] if traces else None,
            })
        results["criteria"]["4"] = {
            "passed": sum(criterion_four_checks),
            "total": 10,
            "checks": criterion_four_checks,
            "evidence": criterion_four_evidence,
        }
    return results


def run_trial(trial_number):
    with tempfile.TemporaryDirectory(prefix=f"provenance-guard-m5-t{trial_number}-") as directory:
        audit_path = Path(directory) / "audit.jsonl"
        results = run_live_criteria(trial_number, audit_path)
        restart = run_restart_check(trial_number, audit_path)
        results["criteria"]["5"] = {
            "passed": int(restart["passed"]),
            "total": 1,
            "checks": [restart["passed"]],
            "evidence": restart,
        }
        results["method"] = {
            "service": "Flask app.py served over HTTP on loopback",
            "signals": "Deterministic local stubs; no external model or API calls",
            "audit_log": "Fresh temporary JSONL file per trial",
        }
        return results


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    all_results = []
    for trial_number in range(1, 4):
        result = run_trial(trial_number)
        output_path = RESULTS / f"unit9_trial_{trial_number}.json"
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        all_results.append(result)
        summary = " ".join(
            f"C{criterion}={data['passed']}/{data['total']}"
            for criterion, data in result["criteria"].items()
        )
        print(f"Trial {trial_number}: {summary} (saved {output_path.relative_to(ROOT)})")
    return int(any(
        result["criteria"][criterion]["passed"] != result["criteria"][criterion]["total"]
        for result in all_results
        for criterion in "12345"
    ))


if __name__ == "__main__":
    raise SystemExit(main())
