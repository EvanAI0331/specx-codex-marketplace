#!/usr/bin/env python3
"""Launch the SpecX MCP server over stdio."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        from scripts.specx_mcp import main as run_mcp
    except ImportError as exc:
        print(
            "SpecX MCP server cannot start because the MCP runtime is missing or invalid. "
            "Install dependencies from requirements.txt and retry.",
            file=sys.stderr,
        )
        print(str(exc), file=sys.stderr)
        return 2
    run_mcp()
    return 0


if __name__ == "__main__":
    sys.exit(main())
