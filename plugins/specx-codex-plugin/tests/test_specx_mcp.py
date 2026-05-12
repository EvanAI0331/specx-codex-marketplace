import asyncio
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.specx_mcp import build_server

VALID = ROOT / "examples" / "generic_research_contract.json"


def run(coro):
    return asyncio.run(coro)


def tool_payload(result):
    if isinstance(result, tuple) and len(result) == 2:
        return result[1]
    return result


class SpecXMcpTests(unittest.TestCase):
    def test_mcp_registers_expected_tools(self):
        server = build_server()
        tools = run(server.list_tools())
        names = {tool.name for tool in tools}
        self.assertEqual(
            names,
            {
                "specx.validate",
                "specx.compile",
                "specx.verify",
                "specx.explain",
            },
        )

    def test_mcp_validate_returns_ok_true_for_valid_contract(self):
        server = build_server()
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        payload = tool_payload(run(server.call_tool("specx.validate", {"contract": contract})))
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["status"], "valid")

    def test_mcp_compile_returns_governed_plan(self):
        server = build_server()
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        payload = tool_payload(run(server.call_tool("specx.compile", {"contract": contract})))
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"]["status"], "compiled")
        self.assertIn("verification_plan", payload["result"])

    def test_mcp_verify_fails_closed_on_missing_constraint(self):
        server = build_server()
        contract = json.loads(VALID.read_text(encoding="utf-8"))
        contract["execution_constraints"]["no_silent_fallback"] = False
        payload = tool_payload(run(server.call_tool("specx.verify", {"contract": contract})))
        self.assertFalse(payload["ok"])
        self.assertIn(
            "no_silent_fallback constraint missing or not true",
            payload["details"],
        )


if __name__ == "__main__":
    unittest.main()
