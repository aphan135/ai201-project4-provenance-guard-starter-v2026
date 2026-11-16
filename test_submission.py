#!/usr/bin/env python3
"""Focused tests for the POST /submit input-validation path."""

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
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["event"], "rejected")
        self.assertEqual(entries[0]["reason"], "punctuation_only_text")
        self.assertNotIn("content_id", entries[0])

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
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["status"], "decided")
        self.assertTrue(entries[0]["content_id"])

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


if __name__ == "__main__":
    unittest.main()
