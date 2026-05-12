# MCP Tools

SpecX exposes four MCP tools:

- `specx.validate`
- `specx.compile`
- `specx.verify`
- `specx.explain`

Each tool accepts a SpecX contract JSON object as `contract`.

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

Validates required fields and array/object shapes. It does not execute the workflow.

### specx.compile

Compiles a valid contract into a governed execution plan with agents, tools, evidence requirements, gates, artifact plan, verification plan, failure semantics, and execution constraints.

### specx.verify

Fails closed when gates, expected artifacts, required agents, required tools, or `no_fake_success` / `no_silent_fallback` constraints are missing.

### specx.explain

Returns a compact explanation with objective summary, domain, task type, counts, risk notes, and unsupported features.

## Failure Boundary

If the MCP runtime is not installed, `scripts/launch_specx_mcp.py` exits non-zero and prints the missing-runtime error. It does not claim that MCP tools are available.
