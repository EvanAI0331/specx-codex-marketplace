# MCP Tools

SpecX exposes four MCP tools:

- `specx.validate`
- `specx.compile`
- `specx.verify`
- `specx.verify_result`
- `specx.explain`
- `specx.init`

Contract tools accept a SpecX contract JSON object as `contract`. `specx.init` accepts `template` and `output`.

## Local Server

Install runtime dependencies:

```bash
python3 -m pip install -r requirements.txt
```

The plugin manifest registers:

```json
{
  "mcpServers": "./.mcp.json"
}
```

The MCP config starts the stdio server:

```json
{
  "mcpServers": {
    "specx": {
      "command": "python3",
      "args": ["./scripts/launch_specx_mcp.py"]
    }
  }
}
```

## Tool Contracts

### specx.validate

Validates Contract Schema v0.1 required fields, gate shape, failure semantics, execution constraints, and verification policy. It does not execute the workflow.

### specx.compile

Compiles a valid contract into a governed execution plan with agents, tools, evidence requirements, gates, artifact plan, verification plan, failure semantics, and execution constraints.

### specx.verify

Fails closed when gates, expected artifacts, required agents, required tools, or `no_fake_success` / `no_silent_fallback` constraints are missing.

### specx.verify_result

Verifies a SpecX execution result against its governing contract. It checks `contract_id`, gate coverage, artifact coverage, verification checks, and status/failure-state semantics.

### specx.init

Creates a verified Contract Schema v0.1 skeleton from `research`, `software_refactor`, or `content_pipeline`.

### specx.explain

Returns a compact explanation with objective summary, domain, task type, counts, risk notes, and unsupported features.

## Failure Boundary

If the MCP runtime is not installed, `scripts/launch_specx_mcp.py` exits non-zero and prints the missing-runtime error. It does not claim that MCP tools are available.

CLI and MCP tools use the same implementation. MCP cannot return a success state that the CLI would reject.
