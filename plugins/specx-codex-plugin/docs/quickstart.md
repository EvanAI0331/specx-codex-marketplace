# Quickstart

SpecX is a governance layer for Codex agents.

## Install

```bash
codex plugin marketplace add https://github.com/BTCNAI/specx-codex-marketplace.git --ref v0.4.0
```

## Initialize A Contract

Install MCP runtime dependencies before using MCP tools:

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 scripts/specx_cli.py init --template research --output ./specx.contract.json
python3 scripts/specx_cli.py init --template software_refactor --output ./specx.contract.json
python3 scripts/specx_cli.py init --template content_pipeline --output ./specx.contract.json
```

## Verify A Contract

```bash
python3 scripts/specx_cli.py verify ./specx.contract.json
```

## Verify An Execution Result

```bash
python3 scripts/specx_cli.py verify-result examples/sample_execution_result_passed.json --contract templates/research.contract.json
```

Expected success:

```json
{
  "ok": true,
  "result": {
    "schema_version": "0.1",
    "status": "verified"
  }
}
```

## Compile A Contract

```bash
python3 scripts/specx_cli.py compile ./specx.contract.json
```

Compilation produces an execution plan with agents, tools, evidence requirements, gates, artifact plan, verification plan, failure semantics, and constraints.

## Verify A Contract

```bash
python3 scripts/specx_cli.py verify ./specx.contract.json
```

Verification fails closed when gates, required agents, artifacts, failure semantics, or `no_fake_success` / `no_silent_fallback` constraints are missing.

## Current Boundary

The current main branch exposes MCP tools:

- `specx.init`
- `specx.validate`
- `specx.compile`
- `specx.verify`
- `specx.verify_result`
- `specx.explain`

See `docs/mcp-tools.md`.
