import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "specx_execution_result_v0_1.schema.json"
PASSED = ROOT / "examples" / "sample_execution_result_passed.json"
FAILED = ROOT / "examples" / "sample_execution_result_failed.json"
BLOCKED = ROOT / "examples" / "sample_execution_result_blocked.json"


class SpecXExecutionResultSchemaV01Tests(unittest.TestCase):
    def test_schema_declares_required_v0_1_fields(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        required = set(schema["required"])
        for field in (
            "result_id",
            "schema_version",
            "contract_id",
            "status",
            "gate_results",
            "artifacts",
            "verification_results",
            "failure_state",
        ):
            self.assertIn(field, required)
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1")

    def test_samples_include_explicit_status_semantics(self):
        passed = json.loads(PASSED.read_text(encoding="utf-8"))
        failed = json.loads(FAILED.read_text(encoding="utf-8"))
        blocked = json.loads(BLOCKED.read_text(encoding="utf-8"))
        self.assertEqual(passed["status"], "passed")
        self.assertIsNone(passed["failure_state"])
        self.assertEqual(failed["status"], "failed")
        self.assertTrue(failed["failure_state"])
        self.assertEqual(blocked["status"], "blocked")
        self.assertTrue(blocked["failure_state"])


if __name__ == "__main__":
    unittest.main()
