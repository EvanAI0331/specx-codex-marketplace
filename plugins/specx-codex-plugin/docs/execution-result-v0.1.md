# Execution Result v0.1

The contract is the pre-execution constraint. The execution result is the post-execution acceptance record.

`verify-result` checks that an execution result is complete and aligned with its governing contract. It does not turn a failed or blocked workflow into success.

## Required Fields

- `result_id`
- `schema_version`: must be `"0.1"`
- `contract_id`
- `status`: `passed`, `failed`, or `blocked`
- `executed_agents`
- `tool_calls`
- `evidence_collected`
- `gate_results`
- `artifacts`
- `verification_results`
- `failure_state`
- `risk_notes`

## Gate Results

Each `gate_results[]` item must include:

- `gate_id`
- `status`
- `evidence`
- `details`

Every contract gate must have a matching gate result.

## Status Semantics

- `passed`: all required contract gates and artifacts are present; `failure_state` must be null or empty.
- `failed`: execution failed; `failure_state` must be non-empty.
- `blocked`: execution stopped because a required gate, evidence item, tool, or approval was unavailable; `failure_state` must be non-empty.

## Fake Success Prevention

`verify-result` prevents fake success by checking:

- `contract_id` matches the contract.
- Every contract gate has a result.
- Every `expected_artifacts` item is represented.
- `passed` results do not carry a failure state.
- `failed` and `blocked` results have an explicit failure state.
- `verification_results` includes `no_fake_success`, `no_silent_fallback`, and `explicit_failure_state`.

## Samples

- `examples/sample_execution_result_passed.json`
- `examples/sample_execution_result_failed.json`
- `examples/sample_execution_result_blocked.json`

Samples are protocol fixtures. They are not proof of real external execution.
