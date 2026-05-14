# SpecX Codex Marketplace

Official Codex Plugin Directory publishing is not yet self-serve.
SpecX is currently distributed through this GitHub-backed Codex marketplace.

## Install

```bash
codex plugin marketplace add https://github.com/BTCNAI/specx-codex-marketplace.git --ref v0.4.0
```

## Included Plugin

- `specx-codex-plugin`

SpecX is a governance layer for Codex agents. It turns vague agent tasks into governed execution contracts, verifies execution results against those contracts, and prevents fake success, silent fallback, and uncontrolled agent execution.

## Marketplace Entry

The marketplace file is:

```text
.agents/plugins/marketplace.json
```

The plugin source is pinned to:

```text
ref: v0.4.0
path: ./plugins/specx-codex-plugin
```
