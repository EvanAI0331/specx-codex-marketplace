import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "specx_cli.py"
VALID = ROOT / "templates" / "software_refactor.contract.json"


def verify_payload(contract):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(contract, handle)
        temp_path = handle.name
    try:
        process = subprocess.run(
            [sys.executable, str(CLI), "verify", temp_path],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        return process.returncode, json.loads(process.stdout)
    finally:
        Path(temp_path).unlink()


class SpecXVerifyTests(unittest.TestCase):
    def test_verify_outputs_ok_true_for_valid_contract(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        code, payload = verify_payload(contract)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])

    def test_verify_failure_lists_required_detail_sections(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        contract.pop("verification_policy")
        contract["gates"][0].pop("on_pass")
        contract["failure_semantics"]["no_silent_fallback"] = False
        code, payload = verify_payload(contract)
        self.assertNotEqual(code, 0)
        self.assertFalse(payload["ok"])
        self.assertIn("missing_fields", payload["details"])
        self.assertIn("invalid_gates", payload["details"])
        self.assertIn("invalid_failure_semantics", payload["details"])
        self.assertIn("invalid_verification_policy", payload["details"])
        self.assertIn("verification_policy", payload["details"]["missing_fields"])
        self.assertTrue(payload["details"]["invalid_gates"])
        self.assertTrue(payload["details"]["invalid_failure_semantics"])


if __name__ == "__main__":
    unittest.main()
