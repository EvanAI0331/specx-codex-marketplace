# Contract Schema v0.1

SpecX Contract Schema v0.1 is the required contract shape for governed workflows.

## Required Fields

- `contract_id`
- `schema_version`: must be `"0.1"`
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

## Gates

Each gate must include:

- `gate_id`
- `condition`
- `on_pass`
- `on_failure`

Missing or malformed gates fail closed.

## Failure Semantics

`failure_semantics` must include:

- `no_fake_success: true`
- `no_silent_fallback: true`
- `explicit_failure_state: true`

`execution_constraints` must include:

- `no_fake_success: true`
- `no_silent_fallback: true`
- `no_hardcoded_fallback: true`

## Verification Policy

`verification_policy.required_checks` must be a non-empty array.

## Fail Closed

Invalid contracts return:

```json
{
  "ok": false,
  "failure_state": "failed_contract_verification",
  "details": {
    "missing_fields": [],
    "invalid_gates": [],
    "invalid_failure_semantics": [],
    "invalid_verification_policy": []
  }
}
```
