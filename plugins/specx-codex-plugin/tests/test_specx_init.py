import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.specx_cli import verify_contract


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "specx_cli.py"


class SpecXInitTests(unittest.TestCase):
    def test_init_creates_valid_contract_for_each_template(self):
        for template in ("research", "software_refactor", "content_pipeline"):
            with self.subTest(template=template):
                with tempfile.TemporaryDirectory() as tmpdir:
                    output = Path(tmpdir) / "specx.contract.json"
                    process = subprocess.run(
                        [
                            sys.executable,
                            str(CLI),
                            "init",
                            "--template",
                            template,
                            "--output",
                            str(output),
                        ],
                        cwd=str(ROOT),
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    payload = json.loads(process.stdout)
                    self.assertEqual(process.returncode, 0)
                    self.assertTrue(payload["ok"])
                    self.assertTrue(output.exists())
                    contract = json.loads(output.read_text(encoding="utf-8"))
                    self.assertTrue(verify_contract(contract)["ok"])


if __name__ == "__main__":
    unittest.main()
