# Contract Format

A SpecX contract is the execution boundary for an agent workflow.

## Required Fields

- `contract_id`
- `schema_version`
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
- `verification_policy`

## Agent Specs

Each item in `required_agents` must define:

- `agent_id`
- `role_spec`
- `execution_spec`
- `output_spec`

An item without LLM-backed decision authority must not be labeled as an agent. Script-only validators, launchers, and transformers are tools.

## Gates

Each gate must define:

- `gate_id`
- `condition`
- `on_pass`
- `on_failure`

Gate failure must return `blocked` or `failed`. It must not be converted into success.

## Failure Semantics

`failure_semantics` must include:

- `no_fake_success: true`
- `no_silent_fallback: true`
- `explicit_failure_state: true`

Use explicit states:

- `blocked`: required input, evidence, spec, approval, or gate is missing.
- `failed`: execution or verification failed.
- `unsupported`: requested capability is not implemented.

## Required Constraints

```json
{
  "execution_constraints": {
    "no_fake_success": true,
    "no_silent_fallback": true,
    "no_hardcoded_fallback": true
  }
}
```

Missing constraints should fail verification.

## Verification Policy

`verification_policy.required_checks` must be a non-empty array. Missing checks fail closed.
