# Quickstart

SpecX is a governance layer for Codex agents.

## Install

```bash
codex plugin marketplace add BTCNAI/specx-codex-marketplace
```

Pinned install:

```bash
codex plugin marketplace add https://github.com/BTCNAI/specx-codex-marketplace.git --ref v0.2.2
```

## Validate A Contract

Install MCP runtime dependencies before using MCP tools:

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 scripts/specx_cli.py validate examples/demo_software_engineering_contract.json
```

Expected success:

```json
{
  "ok": true,
  "result": {
    "contract_id": "demo-software-engineering-001",
    "status": "valid"
  }
}
```

## Compile A Contract

```bash
python3 scripts/specx_cli.py compile examples/demo_software_engineering_contract.json
```

Compilation produces an execution plan with agents, tools, evidence requirements, gates, artifact plan, verification plan, failure semantics, and constraints.

## Verify A Contract

```bash
python3 scripts/specx_cli.py verify examples/demo_software_engineering_contract.json
```

Verification fails closed when gates, required agents, artifacts, failure semantics, or `no_fake_success` / `no_silent_fallback` constraints are missing.

## Current Boundary

The current main branch exposes MCP tools:

- `specx.validate`
- `specx.compile`
- `specx.verify`
- `specx.explain`

See `docs/mcp-tools.md`.
