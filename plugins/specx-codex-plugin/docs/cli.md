# CLI

## specx init

Create a verified Contract Schema v0.1 skeleton from a built-in template:

```bash
python3 scripts/specx_cli.py init --template research --output ./specx.contract.json
python3 scripts/specx_cli.py init --template software_refactor --output ./specx.contract.json
python3 scripts/specx_cli.py init --template content_pipeline --output ./specx.contract.json
```

`init` verifies the template before writing. If the template is invalid, no success is reported.

## specx verify

Verify a contract against schema v0.1 and governance checks:

```bash
python3 scripts/specx_cli.py verify ./specx.contract.json
```

Failure returns `ok=false`, `failure_state`, and structured `details`.

## specx verify-result

Verify an execution result against the governing contract:

```bash
python3 scripts/specx_cli.py verify-result ./specx.execution_result.json --contract ./specx.contract.json
```

`verify-result` checks the execution result schema, contract id, expected artifacts, gate results, verification checks, and failure-state semantics. A complete `failed` or `blocked` result can pass protocol verification while still reporting `execution_status: failed` or `execution_status: blocked`.

## Other Commands

```bash
python3 scripts/specx_cli.py validate ./specx.contract.json
python3 scripts/specx_cli.py compile ./specx.contract.json
python3 scripts/specx_cli.py explain ./specx.contract.json
```

`validate` and `verify` are both fail-closed for v0.1 contracts. `compile` refuses invalid contracts.

## CLI And MCP Consistency

The MCP tools call the same implementation used by the CLI. MCP must not return a success state that the CLI would reject.
