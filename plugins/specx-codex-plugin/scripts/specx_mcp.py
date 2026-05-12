#!/usr/bin/env python3
"""MCP tools for SpecX contract validation, compilation, verification, and explanation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover - exercised by launcher in missing-runtime envs
    raise ImportError("Install the MCP SDK with `python3 -m pip install -r requirements.txt`.") from exc

from scripts.specx_cli import compile_contract, explain_contract, validate_contract, verify_contract


ROOT = Path(__file__).resolve().parents[1]


def build_server() -> FastMCP:
    server = FastMCP(
        "specx-codex-plugin",
        instructions=(
            "SpecX validates, compiles, verifies, and explains governed execution "
            "contracts for Codex agent workflows."
        ),
    )

    @server.tool(
        name="specx.validate",
        description="Validate a SpecX execution contract without executing the workflow.",
    )
    def specx_validate(contract: dict[str, Any]) -> dict[str, Any]:
        return validate_contract(contract)

    @server.tool(
        name="specx.compile",
        description="Compile a valid SpecX contract into a governed execution plan.",
    )
    def specx_compile(contract: dict[str, Any]) -> dict[str, Any]:
        return compile_contract(contract)

    @server.tool(
        name="specx.verify",
        description="Verify a SpecX contract for required gates, artifacts, agents, and failure constraints.",
    )
    def specx_verify(contract: dict[str, Any]) -> dict[str, Any]:
        return verify_contract(contract)

    @server.tool(
        name="specx.explain",
        description="Explain a SpecX contract summary, counts, risks, and unsupported features.",
    )
    def specx_explain(contract: dict[str, Any]) -> dict[str, Any]:
        return explain_contract(contract)

    return server


mcp = build_server()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
