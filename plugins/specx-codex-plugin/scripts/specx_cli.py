#!/usr/bin/env python3
"""SpecX CLI for SpecX contract and execution-result governance."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "0.1"
EXECUTION_RESULT_SCHEMA_VERSION = "0.1"
TEMPLATE_NAMES = ("research", "software_refactor", "content_pipeline")
TEMPLATE_FILES = {
    "research": ROOT / "templates" / "research.contract.json",
    "software_refactor": ROOT / "templates" / "software_refactor.contract.json",
    "content_pipeline": ROOT / "templates" / "content_pipeline.contract.json",
}

REQUIRED_CONTRACT_FIELDS = [
    "contract_id",
    "schema_version",
    "objective",
    "domain",
    "task_type",
    "required_agents",
    "required_tools",
    "required_evidence",
    "gates",
    "expected_artifacts",
    "failure_semantics",
    "execution_constraints",
    "human_approval",
    "verification_policy",
]
NON_EMPTY_ARRAY_FIELDS = [
    "required_agents",
    "required_tools",
    "required_evidence",
    "gates",
    "expected_artifacts",
]
REQUIRED_GATE_FIELDS = ["gate_id", "condition", "on_pass", "on_failure"]
REQUIRED_FAILURE_SEMANTICS = [
    "no_fake_success",
    "no_silent_fallback",
    "explicit_failure_state",
]
REQUIRED_EXECUTION_CONSTRAINTS = [
    "no_fake_success",
    "no_silent_fallback",
    "no_hardcoded_fallback",
]
REQUIRED_EXECUTION_RESULT_FIELDS = [
    "result_id",
    "schema_version",
    "contract_id",
    "status",
    "executed_agents",
    "tool_calls",
    "evidence_collected",
    "gate_results",
    "artifacts",
    "verification_results",
    "failure_state",
    "risk_notes",
]
EXECUTION_RESULT_STATUSES = {"passed", "failed", "blocked"}
REQUIRED_GATE_RESULT_FIELDS = ["gate_id", "status", "evidence", "details"]
REQUIRED_RESULT_CHECKS = [
    "no_fake_success",
    "no_silent_fallback",
    "explicit_failure_state",
]


def ok(result: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, "result": result}


def fail(error: str, failure_state: str, details: dict[str, Any] | list[Any] | None = None) -> dict[str, Any]:
    return {
        "ok": False,
        "error": error,
        "failure_state": failure_state,
        "details": details or {},
    }


def load_json(path: str | Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    input_path = Path(path)
    try:
        with input_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        return None, fail("Input file not found.", "failed_input_not_found", {"path": str(input_path)})
    except json.JSONDecodeError as exc:
        return None, fail(
            "Input is not valid JSON.",
            "failed_invalid_json",
            {"path": str(input_path), "message": str(exc)},
        )
    if not isinstance(payload, dict):
        return None, fail("Contract must be a JSON object.", "failed_invalid_contract_type")
    return payload, None


def empty_governance_details() -> dict[str, Any]:
    return {
        "missing_fields": [],
        "invalid_gates": [],
        "invalid_failure_semantics": [],
        "invalid_verification_policy": [],
        "invalid_execution_constraints": [],
        "invalid_types": [],
    }


def empty_result_details() -> dict[str, Any]:
    return {
        "missing_fields": [],
        "invalid_types": [],
        "invalid_status": [],
        "invalid_gate_results": [],
        "missing_gate_results": [],
        "invalid_artifacts": [],
        "missing_artifacts": [],
        "invalid_verification_results": [],
        "contract_mismatch": [],
        "invalid_failure_state": [],
    }


def governance_details(contract: dict[str, Any]) -> dict[str, Any]:
    details = empty_governance_details()

    for field in REQUIRED_CONTRACT_FIELDS:
        if field not in contract:
            details["missing_fields"].append(field)

    if contract.get("schema_version") != SCHEMA_VERSION:
        details["invalid_types"].append(
            {
                "field": "schema_version",
                "expected": SCHEMA_VERSION,
                "actual": contract.get("schema_version"),
            }
        )

    for field in NON_EMPTY_ARRAY_FIELDS:
        if field in contract and (not isinstance(contract[field], list) or not contract[field]):
            details["invalid_types"].append(
                {"field": field, "expected": "non-empty array", "actual": type(contract[field]).__name__}
            )
            if field == "gates":
                details["invalid_gates"].append({"error": "gates must be a non-empty array"})

    for field in ("failure_semantics", "execution_constraints", "human_approval", "verification_policy"):
        if field in contract and not isinstance(contract[field], dict):
            details["invalid_types"].append(
                {"field": field, "expected": "object", "actual": type(contract[field]).__name__}
            )

    gates = contract.get("gates")
    if isinstance(gates, list):
        for index, gate in enumerate(gates):
            if not isinstance(gate, dict):
                details["invalid_gates"].append(
                    {"gate_index": index, "error": "gate must be an object"}
                )
                continue
            missing = [field for field in REQUIRED_GATE_FIELDS if field not in gate]
            if missing:
                details["invalid_gates"].append({"gate_index": index, "missing_fields": missing})
    elif "gates" in contract:
        details["invalid_gates"].append({"error": "gates must be a non-empty array"})

    failure_semantics = contract.get("failure_semantics")
    if isinstance(failure_semantics, dict):
        for name in REQUIRED_FAILURE_SEMANTICS:
            if failure_semantics.get(name) is not True:
                details["invalid_failure_semantics"].append(
                    {"field": name, "expected": True, "actual": failure_semantics.get(name)}
                )
    elif "failure_semantics" in contract:
        details["invalid_failure_semantics"].append({"error": "failure_semantics must be an object"})

    execution_constraints = contract.get("execution_constraints")
    if isinstance(execution_constraints, dict):
        for name in REQUIRED_EXECUTION_CONSTRAINTS:
            if execution_constraints.get(name) is not True:
                details["invalid_execution_constraints"].append(
                    {"field": name, "expected": True, "actual": execution_constraints.get(name)}
                )
    elif "execution_constraints" in contract:
        details["invalid_execution_constraints"].append({"error": "execution_constraints must be an object"})

    verification_policy = contract.get("verification_policy")
    if isinstance(verification_policy, dict):
        checks = verification_policy.get("required_checks")
        if not isinstance(checks, list) or not checks:
            details["invalid_verification_policy"].append(
                {"field": "required_checks", "expected": "non-empty array", "actual": checks}
            )
    elif "verification_policy" in contract:
        details["invalid_verification_policy"].append({"error": "verification_policy must be an object"})
    else:
        details["invalid_verification_policy"].append({"field": "required_checks", "error": "missing"})

    return details


def has_errors(details: dict[str, Any]) -> bool:
    return any(bool(value) for value in details.values())


def item_id(item: Any, preferred_keys: tuple[str, ...]) -> str | None:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        for key in preferred_keys:
            value = item.get(key)
            if isinstance(value, str) and value:
                return value
    return None


def result_details(result: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    details = empty_result_details()

    for field in REQUIRED_EXECUTION_RESULT_FIELDS:
        if field not in result:
            details["missing_fields"].append(field)

    if result.get("schema_version") != EXECUTION_RESULT_SCHEMA_VERSION:
        details["invalid_types"].append(
            {
                "field": "schema_version",
                "expected": EXECUTION_RESULT_SCHEMA_VERSION,
                "actual": result.get("schema_version"),
            }
        )

    if result.get("contract_id") != contract.get("contract_id"):
        details["contract_mismatch"].append(
            {
                "field": "contract_id",
                "expected": contract.get("contract_id"),
                "actual": result.get("contract_id"),
            }
        )

    status = result.get("status")
    if status not in EXECUTION_RESULT_STATUSES:
        details["invalid_status"].append(
            {"field": "status", "expected": sorted(EXECUTION_RESULT_STATUSES), "actual": status}
        )

    for field in (
        "executed_agents",
        "tool_calls",
        "evidence_collected",
        "gate_results",
        "artifacts",
        "risk_notes",
    ):
        if field in result and not isinstance(result[field], list):
            details["invalid_types"].append(
                {"field": field, "expected": "array", "actual": type(result[field]).__name__}
            )

    if "verification_results" in result and not isinstance(result["verification_results"], dict):
        details["invalid_types"].append(
            {
                "field": "verification_results",
                "expected": "object",
                "actual": type(result["verification_results"]).__name__,
            }
        )

    failure_state = result.get("failure_state")
    if status == "passed" and failure_state not in (None, ""):
        details["invalid_failure_state"].append(
            {"status": status, "expected": "empty or null", "actual": failure_state}
        )
    if status in {"failed", "blocked"} and not failure_state:
        details["invalid_failure_state"].append(
            {"status": status, "expected": "non-empty failure_state", "actual": failure_state}
        )

    expected_gate_ids = [
        item_id(gate, ("gate_id",)) for gate in contract.get("gates", []) if item_id(gate, ("gate_id",))
    ]
    seen_gate_ids = set()
    gate_results = result.get("gate_results")
    if isinstance(gate_results, list):
        for index, gate_result in enumerate(gate_results):
            if not isinstance(gate_result, dict):
                details["invalid_gate_results"].append(
                    {"gate_result_index": index, "error": "gate_result must be an object"}
                )
                continue
            missing = [field for field in REQUIRED_GATE_RESULT_FIELDS if field not in gate_result]
            if missing:
                details["invalid_gate_results"].append(
                    {"gate_result_index": index, "missing_fields": missing}
                )
            gate_id = gate_result.get("gate_id")
            if gate_id:
                seen_gate_ids.add(gate_id)
            if gate_result.get("status") not in EXECUTION_RESULT_STATUSES:
                details["invalid_gate_results"].append(
                    {
                        "gate_result_index": index,
                        "field": "status",
                        "expected": sorted(EXECUTION_RESULT_STATUSES),
                        "actual": gate_result.get("status"),
                    }
                )
            if status == "passed" and gate_result.get("status") != "passed":
                details["invalid_gate_results"].append(
                    {
                        "gate_id": gate_id,
                        "error": "passed execution_result cannot contain non-passed gate_result",
                    }
                )
    missing_gate_ids = sorted(set(expected_gate_ids) - seen_gate_ids)
    if missing_gate_ids:
        details["missing_gate_results"].extend(missing_gate_ids)

    expected_artifact_ids = {
        artifact_id
        for artifact_id in (
            item_id(artifact, ("artifact_id", "id", "name"))
            for artifact in contract.get("expected_artifacts", [])
        )
        if artifact_id
    }
    artifact_ids = set()
    artifacts = result.get("artifacts")
    if isinstance(artifacts, list):
        for index, artifact in enumerate(artifacts):
            artifact_id = item_id(artifact, ("artifact_id", "id", "name"))
            if artifact_id is None:
                details["invalid_artifacts"].append(
                    {"artifact_index": index, "error": "artifact must have artifact_id/id/name or be a string"}
                )
                continue
            artifact_ids.add(artifact_id)
    missing_artifacts = sorted(expected_artifact_ids - artifact_ids)
    if missing_artifacts:
        details["missing_artifacts"].extend(missing_artifacts)

    verification_results = result.get("verification_results")
    if isinstance(verification_results, dict):
        for check in REQUIRED_RESULT_CHECKS:
            value = verification_results.get(check)
            if value is not True:
                details["invalid_verification_results"].append(
                    {"field": check, "expected": True, "actual": value}
                )
    elif "verification_results" in result:
        details["invalid_verification_results"].append(
            {"error": "verification_results must be an object"}
        )

    return details


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    details = governance_details(contract)
    if has_errors(details):
        return fail("Contract validation failed.", "failed_contract_invalid", details)
    return ok(
        {
            "contract_id": contract["contract_id"],
            "schema_version": contract["schema_version"],
            "status": "valid",
        }
    )


def verify_contract(contract: dict[str, Any]) -> dict[str, Any]:
    details = governance_details(contract)
    if has_errors(details):
        return fail("Contract verification failed.", "failed_contract_verification", details)
    return ok(
        {
            "contract_id": contract["contract_id"],
            "schema_version": contract["schema_version"],
            "status": "verified",
        }
    )


def compile_contract(contract: dict[str, Any]) -> dict[str, Any]:
    verification = verify_contract(contract)
    if not verification["ok"]:
        return verification
    plan = {
        "plan_id": "plan-" + str(contract["contract_id"]),
        "contract_id": contract["contract_id"],
        "schema_version": contract["schema_version"],
        "objective": contract["objective"],
        "domain": contract["domain"],
        "task_type": contract["task_type"],
        "agents": contract["required_agents"],
        "tools": contract["required_tools"],
        "evidence_requirements": contract["required_evidence"],
        "gates": contract["gates"],
        "artifact_plan": contract["expected_artifacts"],
        "verification_plan": {
            "required_checks": contract["verification_policy"]["required_checks"],
            "required_gate_checks": [gate["gate_id"] for gate in contract["gates"]],
            "required_evidence": contract["required_evidence"],
            "required_artifacts": contract["expected_artifacts"],
        },
        "failure_semantics": contract["failure_semantics"],
        "execution_constraints": contract["execution_constraints"],
        "human_approval": contract["human_approval"],
        "status": "compiled",
    }
    return ok(plan)


def explain_contract(contract: dict[str, Any]) -> dict[str, Any]:
    verification = verify_contract(contract)
    risk_notes = []
    if not verification["ok"]:
        risk_notes.append("Contract has validation or governance errors.")
    result = {
        "summary": contract.get("objective", ""),
        "schema_version": contract.get("schema_version"),
        "domain": contract.get("domain"),
        "task_type": contract.get("task_type"),
        "agent_count": len(contract.get("required_agents", [])) if isinstance(contract.get("required_agents"), list) else 0,
        "tool_count": len(contract.get("required_tools", [])) if isinstance(contract.get("required_tools"), list) else 0,
        "gate_count": len(contract.get("gates", [])) if isinstance(contract.get("gates"), list) else 0,
        "artifact_count": len(contract.get("expected_artifacts", []))
        if isinstance(contract.get("expected_artifacts"), list)
        else 0,
        "verification_ok": verification["ok"],
        "failure_state": verification.get("failure_state"),
        "risk_notes": risk_notes,
        "unsupported_features": contract.get("unsupported_features", []) if isinstance(contract, dict) else [],
    }
    return ok(result)


def init_contract(template: str, output: str | Path) -> dict[str, Any]:
    template_path = TEMPLATE_FILES.get(template)
    if template_path is None:
        return fail(
            "Unknown template.",
            "failed_unknown_template",
            {"template": template, "allowed_templates": list(TEMPLATE_NAMES)},
        )
    contract, error = load_json(template_path)
    if error:
        return error
    verification = verify_contract(contract)
    if not verification["ok"]:
        return fail("Template verification failed.", "failed_invalid_template", verification["details"])

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ok(
        {
            "status": "initialized",
            "template": template,
            "output": str(output_path),
            "contract_id": contract["contract_id"],
            "schema_version": contract["schema_version"],
        }
    )


def verify_execution_result(execution_result: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    contract_verification = verify_contract(contract)
    if not contract_verification["ok"]:
        return fail(
            "Contract verification failed before execution_result verification.",
            "failed_contract_verification",
            {"contract_details": contract_verification["details"]},
        )

    details = result_details(execution_result, contract)
    if has_errors(details):
        return fail("Execution result verification failed.", "failed_execution_result_verification", details)

    return ok(
        {
            "result_id": execution_result["result_id"],
            "contract_id": execution_result["contract_id"],
            "schema_version": execution_result["schema_version"],
            "execution_status": execution_result["status"],
            "status": "verified",
        }
    )


def run(command: str, path: str | Path) -> dict[str, Any]:
    contract, error = load_json(path)
    if error:
        return error
    if command == "validate":
        return validate_contract(contract)
    if command == "compile":
        return compile_contract(contract)
    if command == "verify":
        return verify_contract(contract)
    if command == "explain":
        return explain_contract(contract)
    return fail("Unsupported command.", "failed_unsupported_command", {"command": command})


def run_verify_result(result_path: str | Path, contract_path: str | Path) -> dict[str, Any]:
    execution_result, result_error = load_json(result_path)
    if result_error:
        return result_error
    contract, contract_error = load_json(contract_path)
    if contract_error:
        return contract_error
    return verify_execution_result(execution_result, contract)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SpecX contract CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a verified SpecX v0.1 contract from a template")
    init_parser.add_argument("--template", required=True, choices=TEMPLATE_NAMES)
    init_parser.add_argument("--output", required=True)

    for command in ("validate", "compile", "verify", "explain"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("path")

    verify_result_parser = subparsers.add_parser(
        "verify-result",
        help="Verify a SpecX execution_result v0.1 against a SpecX contract",
    )
    verify_result_parser.add_argument("path")
    verify_result_parser.add_argument("--contract", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        response = init_contract(args.template, args.output)
    elif args.command == "verify-result":
        response = run_verify_result(args.path, args.contract)
    else:
        response = run(args.command, args.path)
    print(json.dumps(response, indent=2, sort_keys=True))
    return 0 if response.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
