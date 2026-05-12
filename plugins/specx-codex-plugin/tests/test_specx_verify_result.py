import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.specx_cli import verify_execution_result


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "specx_cli.py"
CONTRACT = ROOT / "templates" / "research.contract.json"
PASSED = ROOT / "examples" / "sample_execution_result_passed.json"
FAILED = ROOT / "examples" / "sample_execution_result_failed.json"


def load_pair():
    return (
        json.loads(PASSED.read_text(encoding="utf-8")),
        json.loads(CONTRACT.read_text(encoding="utf-8")),
    )


class SpecXVerifyResultTests(unittest.TestCase):
    def test_valid_passed_result_passes(self):
        result, contract = load_pair()
        payload = verify_execution_result(result, contract)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["execution_status"], "passed")

    def test_failed_result_with_failure_state_is_protocol_valid(self):
        result = json.loads(FAILED.read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        payload = verify_execution_result(result, contract)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["execution_status"], "failed")

    def test_missing_artifact_fails(self):
        result, contract = load_pair()
        result["artifacts"] = result["artifacts"][:-1]
        payload = verify_execution_result(result, contract)
        self.assertFalse(payload["ok"])
        self.assertIn("decision_packet", payload["details"]["missing_artifacts"])

    def test_missing_gate_result_fails(self):
        result, contract = load_pair()
        result["gate_results"] = result["gate_results"][:-1]
        payload = verify_execution_result(result, contract)
        self.assertFalse(payload["ok"])
        self.assertIn("decision_packet_gate", payload["details"]["missing_gate_results"])

    def test_passed_with_failure_state_fails(self):
        result, contract = load_pair()
        result["failure_state"] = "fake_success_with_failure"
        payload = verify_execution_result(result, contract)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["details"]["invalid_failure_state"])

    def test_failed_without_failure_state_fails(self):
        result, contract = load_pair()
        result["status"] = "failed"
        result["failure_state"] = None
        payload = verify_execution_result(result, contract)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["details"]["invalid_failure_state"])

    def test_result_contract_id_mismatch_fails(self):
        result, contract = load_pair()
        result["contract_id"] = "different-contract"
        payload = verify_execution_result(result, contract)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["details"]["contract_mismatch"])

    def test_cli_verify_result(self):
        process = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "verify-result",
                str(PASSED),
                "--contract",
                str(CONTRACT),
            ],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        payload = json.loads(process.stdout)
        self.assertEqual(process.returncode, 0)
        self.assertTrue(payload["ok"])

    def test_cli_verify_result_fails_closed(self):
        result, _ = load_pair()
        invalid = copy.deepcopy(result)
        invalid["verification_results"]["no_fake_success"] = False
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(invalid, handle)
            temp_path = handle.name
        try:
            process = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "verify-result",
                    temp_path,
                    "--contract",
                    str(CONTRACT),
                ],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                check=False,
            )
            payload = json.loads(process.stdout)
            self.assertNotEqual(process.returncode, 0)
            self.assertFalse(payload["ok"])
            self.assertTrue(payload["details"]["invalid_verification_results"])
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    unittest.main()
