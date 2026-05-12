import json
import unittest
from pathlib import Path

from scripts.specx_cli import verify_contract


ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "templates" / "research.contract.json"
SCHEMA = ROOT / "schemas" / "specx_contract_v0_1.schema.json"


class SpecXSchemaV01Tests(unittest.TestCase):
    def test_schema_file_declares_required_v0_1_fields(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        required = set(schema["required"])
        self.assertIn("schema_version", required)
        self.assertIn("verification_policy", required)
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1")

    def test_valid_contract_passes(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        payload = verify_contract(contract)
        self.assertTrue(payload["ok"])

    def test_missing_required_field_fails(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        contract.pop("objective")
        payload = verify_contract(contract)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["failure_state"], "failed_contract_verification")
        self.assertIn("objective", payload["details"]["missing_fields"])

    def test_missing_gates_fails(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        contract["gates"] = []
        payload = verify_contract(contract)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["details"]["invalid_types"])

    def test_missing_no_fake_success_fails(self):
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        contract["failure_semantics"].pop("no_fake_success")
        payload = verify_contract(contract)
        self.assertFalse(payload["ok"])
        self.assertTrue(payload["details"]["invalid_failure_semantics"])


if __name__ == "__main__":
    unittest.main()
