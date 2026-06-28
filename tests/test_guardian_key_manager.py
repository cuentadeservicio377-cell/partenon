"""Tests for Guardian key audit and model recommendation utilities."""

import unittest

from mcp_servers.security.key_manager import (
    audit_key_strength,
    detect_key_provider,
    recommend_model,
)
from mcp_servers.security.server import (
    security_audit_key_strength,
    security_detect_key_provider,
    security_recommend_model,
)


class GuardianKeyManagerTestCase(unittest.TestCase):
    def test_detect_stripe_key(self):
        self.assertEqual(detect_key_provider("sk_test_12345"), "stripe")

    def test_detect_openai_key(self):
        self.assertEqual(detect_key_provider("sk-12345"), "openai")

    def test_detect_unknown_key(self):
        self.assertEqual(detect_key_provider("abcdef"), "unknown")

    def test_audit_strong_key(self):
        result = audit_key_strength("sk_live_" + "a" * 64)
        self.assertEqual(result["provider"], "stripe")
        self.assertGreaterEqual(result["score"], 80)
        self.assertEqual(result["recommendation"], "ok")

    def test_audit_weak_key(self):
        result = audit_key_strength("password")
        self.assertLess(result["score"], 50)
        self.assertEqual(result["recommendation"], "rotate immediately")

    def test_recommend_model(self):
        result = recommend_model("anthropic", "standard", "normal")
        self.assertEqual(result["provider"], "anthropic")
        self.assertIn("model", result)

    def test_server_audit_key_strength_tool(self):
        result = security_audit_key_strength("sk-test-" + "x" * 64)
        self.assertTrue(result["ok"])
        self.assertIn("score", result)

    def test_server_detect_provider_tool(self):
        result = security_detect_key_provider("nvapi-12345")
        self.assertTrue(result["ok"])
        self.assertEqual(result["provider"], "nvidia")

    def test_server_recommend_model_tool(self):
        result = security_recommend_model("google", "cheap", "low")
        self.assertTrue(result["ok"])
        self.assertIn("model", result)


if __name__ == "__main__":
    unittest.main()
