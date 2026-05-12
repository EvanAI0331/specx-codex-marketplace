import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "specx_cli.py"
VALID = ROOT / "templates" / "research.contract.json"


def run_cli(*args):
    process = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    payload = json.loads(process.stdout)
    return process.returncode, payload


class SpecXCliTests(unittest.TestCase):
    def test_validate_valid_contract_returns_ok_true(self):
        code, payload = run_cli("validate", str(VALID))
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["schema_version"], "0.1")

    def test_compile_returns_status_compiled(self):
        code, payload = run_cli("compile", str(VALID))
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["status"], "compiled")
        self.assertIn("verification_plan", payload["result"])

    def test_explain_returns_summary(self):
        code, payload = run_cli("explain", str(VALID))
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertIn("summary", payload["result"])

    def test_legacy_positional_shape_is_rejected_by_argparse(self):
        process = subprocess.run(
            [sys.executable, str(CLI), "init", str(VALID)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(process.returncode, 0)


if __name__ == "__main__":
    unittest.main()
