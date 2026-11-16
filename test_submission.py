#!/usr/bin/env python3
"""Focused tests for the POST /submit input-validation path."""

import hashlib
import sys
import tempfile
import types
import unittest
import uuid
from pathlib import Path
from unittest.mock import Mock, patch

import app
import audit
import config


class SubmitValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.audit_path_patch = patch.object(
            config,
            "AUDIT_LOG",
            Path(self.temp_dir.name) / "audit.jsonl",
        )
        self.audit_path_patch.start()
        self.addCleanup(self.audit_path_patch.stop)
        self.client = app.app.test_client()

    def _signals(self, model_score=0.3, style_score=0.4):
        detector = types.ModuleType("detector")
        detector.DetectorUnavailable = type("DetectorUnavailable", (Exception,), {})
        detector.model_signal = Mock(return_value=model_score)

        stylometry = types.ModuleType("stylometry")
        stylometry.style_signal = Mock(return_value=style_score)
        return detector, stylometry

    def _submit(self, text):
        return self.client.post(
            "/submit",
            json={"text": text, "creator_id": uuid.uuid4().hex},
        )

    def _run_entry(self):
        return next(
            entry for entry in audit.read_entries()
            if entry.get("event") == "run"
        )

    def test_punctuation_only_text_is_rejected_and_audited_before_scoring(self):
        detector, stylometry = self._signals()
        with patch.dict(
            sys.modules,
            {"detector": detector, "stylometry": stylometry},
        ):
            response = self._submit("... !!!")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "punctuation_only_text")
        detector.model_signal.assert_not_called()
        stylometry.style_signal.assert_not_called()
        entries = audit.read_entries()
        rejection = next(entry for entry in entries if entry.get("event") == "rejected")
        self.assertEqual(rejection["reason"], "punctuation_only_text")
        self.assertNotIn("content_id", rejection)
        run = self._run_entry()
        self.assertEqual(run["http_status"], 400)
        self.assertEqual(run["output"], response.json)
        self.assertEqual(run["input"]["text_length"], len("... !!!"))
        self.assertEqual(
            run["input"]["text_sha256"],
            hashlib.sha256("... !!!".encode("utf-8")).hexdigest(),
        )
        self.assertNotIn("text", run["input"])
        self.assertGreaterEqual(run["duration_ms"], 0)

    def test_unicode_punctuation_and_whitespace_are_rejected(self):
        detector, stylometry = self._signals()
        with patch.dict(
            sys.modules,
            {"detector": detector, "stylometry": stylometry},
        ):
            response = self._submit("  ！？—…  ")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "punctuation_only_text")
        detector.model_signal.assert_not_called()
        stylometry.style_signal.assert_not_called()
        self.assertEqual(self._run_entry()["http_status"], 400)

    def test_valid_text_still_scores_and_logs_a_decision(self):
        detector, stylometry = self._signals()
        with patch.dict(
            sys.modules,
            {"detector": detector, "stylometry": stylometry},
        ):
            response = self._submit("This is an ordinary sentence.")

        self.assertEqual(response.status_code, 200)
        detector.model_signal.assert_called_once_with("This is an ordinary sentence.")
        stylometry.style_signal.assert_called_once_with("This is an ordinary sentence.")
        entries = audit.read_entries()
        decision = next(entry for entry in entries if entry.get("status") == "decided")
        self.assertTrue(decision["content_id"])
        run = self._run_entry()
        self.assertEqual(run["http_status"], 200)
        self.assertEqual(run["output"], response.json)
        self.assertEqual(run["detector_model"], config.DETECTOR_MODEL)

    def test_empty_text_keeps_existing_invalid_text_response(self):
        detector, stylometry = self._signals()
        with patch.dict(
            sys.modules,
            {"detector": detector, "stylometry": stylometry},
        ):
            response = self._submit("   ")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "invalid_text")
        detector.model_signal.assert_not_called()
        stylometry.style_signal.assert_not_called()
        self.assertEqual(self._run_entry()["output"], response.json)

    def test_unhandled_failure_is_logged_as_a_failed_run(self):
        detector, stylometry = self._signals()
        detector.model_signal.side_effect = RuntimeError("model process failed")
        with patch.dict(
            sys.modules,
            {"detector": detector, "stylometry": stylometry},
        ), patch.dict(app.app.config, {"PROPAGATE_EXCEPTIONS": False}):
            response = self._submit("This request triggers a model error.")

        self.assertEqual(response.status_code, 500)
        run = self._run_entry()
        self.assertEqual(run["http_status"], 500)
        self.assertEqual(run["output"]["content_type"], "text/html; charset=utf-8")
        self.assertEqual(run["output"]["body_chars"], len(response.get_data()))


if __name__ == "__main__":
    unittest.main()
