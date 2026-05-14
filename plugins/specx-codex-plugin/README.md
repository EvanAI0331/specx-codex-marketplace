# SpecX Codex Plugin

Official Codex Plugin Directory publishing is not yet self-serve.
SpecX is currently distributed through a GitHub-backed Codex marketplace.

SpecX turns vague agent tasks into governed execution contracts.
It enforces required agents, tools, evidence, gates, artifacts, and failure semantics.
It prevents fake success, silent fallback, and uncontrolled agent execution.

SpecX is a governance layer for Codex agents.

## Install

```bash
codex plugin marketplace add https://github.com/BTCNAI/specx-codex-marketplace.git --ref v0.4.0
```

The official Codex directory will be used after OpenAI opens self-serve publishing.

## What It Provides

- Contract-first workflow definition.
- Required LLM-backed agents with role, execution, and output specs.
- Gate-bound and evidence-bound decisions.
- Artifact contracts and explicit failure states.
- Fail-closed verification for fake success and silent fallback.

## Current Shape

The current main branch provides skills + CLI + MCP tools.

Included skills:

- `specx-contract-compiler`
- `specx-runtime`
- `specx-agent-governance`
- `specx-verifier`

Included CLI:

```bash
python3 scripts/specx_cli.py init --template research --output ./specx.contract.json
python3 scripts/specx_cli.py init --template software_refactor --output ./specx.contract.json
python3 scripts/specx_cli.py init --template content_pipeline --output ./specx.contract.json
python3 scripts/specx_cli.py verify ./specx.contract.json
python3 scripts/specx_cli.py verify-result ./specx.execution_result.json --contract ./specx.contract.json
python3 scripts/specx_cli.py validate examples/demo_software_engineering_contract.json
python3 scripts/specx_cli.py compile examples/demo_software_engineering_contract.json
python3 scripts/specx_cli.py explain examples/demo_software_engineering_contract.json
```

Included MCP tools:

- `specx.validate`
- `specx.compile`
- `specx.verify`
- `specx.verify_result`
- `specx.explain`
- `specx.init`

Install MCP runtime dependencies before running MCP tools:

```bash
python3 -m pip install -r requirements.txt
```

## Contract Shape

Every valid contract must define:

- `contract_id`
- `schema_version: "0.1"`
- `objective`
- `domain`
- `task_type`
- `required_agents`
- `required_tools`
- `required_evidence`
- `gates`
- `expected_artifacts`
- `failure_semantics`
- `execution_constraints`
- `human_approval`
- `verification_policy.required_checks`

Each gate must include `gate_id`, `condition`, `on_pass`, and `on_failure`. `failure_semantics` must include `no_fake_success`, `no_silent_fallback`, and `explicit_failure_state`.

If required evidence, tools, specs, gates, artifacts, or verification policy are missing, the workflow must return `ok=false` with `failure_state` and `details`. It must not claim success.

## Execution Result Shape

Contracts are pre-execution constraints. Execution results are post-execution acceptance records.

`verify-result` checks that a result has matching `contract_id`, gate results for every contract gate, artifacts for every expected artifact, explicit status, failure semantics checks, and correct `failure_state` behavior.

Execution statuses:

- `passed`: every required gate and artifact is present; `failure_state` must be null or empty.
- `failed`: execution failed; `failure_state` must be explicit.
- `blocked`: execution stopped before completion; `failure_state` must be explicit.

## Demos

Demo 1: Software engineering

- Before: "Refactor this backend."
- After SpecX: required agents, gates, tests, failure semantics, and artifact contract.
- File: `examples/demo_software_engineering_contract.json`

Demo 2: Research task

- Before: "Research this market."
- After SpecX: evidence requirements, source gates, decision packet, and risk notes.
- File: `examples/demo_research_task_contract.json`

Demo 3: Multi-agent system

- Before: agents freestyle.
- After SpecX: contract-first runtime, verifier, and explicit failure state.
- File: `examples/demo_multi_agent_system_contract.json`

## Docs

- `docs/quickstart.md`
- `docs/contract-format.md`
- `docs/use-cases.md`
- `docs/comparison.md`
- `docs/mcp-tools.md`
- `docs/contract-schema-v0.1.md`
- `docs/execution-result-v0.1.md`
- `docs/cli.md`

## Roadmap

P0:

- Contract schema v0.1 adoption feedback.
- Execution result adoption feedback.
- MCP integration tests against real Codex marketplace install.

P1:

- `specx init`
- `specx verify`

The next release target is a tagged MCP release after install testing.

## Repository Structure

```text
specx-codex-plugin/
├── .codex-plugin/plugin.json
├── docs/
├── skills/
├── scripts/
├── schemas/
├── templates/
├── examples/
├── tests/
├── README.md
├── marketplace.json
├── LICENSE
├── requirements.txt
└── .mcp.json
```

## Failure Policy

SpecX must not replace agent decisions with hardcoded fallback logic. Scripts may validate, transform, launch, or verify; they must not impersonate agent reasoning.

No LLM-backed decision authority means no agent label.
