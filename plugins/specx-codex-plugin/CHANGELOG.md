# Changelog

## 0.4.0

- Added Execution Result Schema v0.1 at `schemas/specx_execution_result_v0_1.schema.json`.
- Added `specx verify-result` to verify execution results against their governing contract.
- Added MCP `specx.verify_result` with the same implementation as CLI `verify-result`.
- Added passed, failed, and blocked execution-result samples.
- Added GitHub Actions CI for pytest, contract validation, compilation, verification, and result verification.
- Added tests for execution-result schema and fail-closed result verification.

## 0.3.0

- Added Contract Schema v0.1 at `schemas/specx_contract_v0_1.schema.json`.
- Added verified templates for research, software refactor, and content pipeline contracts.
- Added `specx init` CLI support through `scripts/specx_cli.py init`.
- Upgraded `specx verify` to fail closed with `failure_state` and structured details.
- Added MCP `specx.init` and aligned MCP behavior with CLI behavior.
- Added tests for schema v0.1, init, verify, and MCP fail-closed behavior.

## 0.2.2

- Added real MCP tools for validate, compile, verify, and explain.
