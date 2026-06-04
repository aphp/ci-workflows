#!/usr/bin/env python3

import json
import sys
from pathlib import Path

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("trivy-license-results.sarif")
max_len = 200

try:
    with path.open("r", encoding="utf-8") as f:
        sarif = json.load(f)

except FileNotFoundError:
    print(f"ERROR: SARIF file not found: {path}")
    sys.exit(1)

except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON in SARIF file: {path}")
    print(f"Details: {e}")
    sys.exit(1)

total_id_fixed = 0
total_ruleId_fixed = 0

for run in sarif.get("runs", []):

    # Check if id is short enough
    for rule in run.get("tool", {}).get("driver", {}).get("rules", []):
        if isinstance(rule.get("id"), str) and len(rule["id"]) > max_len:
            rule.setdefault("properties", {})["originalTrivyRuleId"] = rule["id"]
            rule["id"] = rule["id"][:max_len]
            total_id_fixed += 1

    # Check if ruleId is short enough
    for result in run.get("results", []):
        if isinstance(result.get("ruleId"), str) and len(result["ruleId"]) > max_len:
            result.setdefault("properties", {})["originalTrivyRuleId"] = result["ruleId"]
            result["ruleId"] = result["ruleId"][:max_len]
            total_ruleId_fixed += 1


with path.open("w", encoding="utf-8") as f:
    json.dump(sarif, f, ensure_ascii=False, indent=2)



print("SARIF patched")
print(f"id fixed: {total_id_fixed}")
print(f"ruleId fixed: {total_ruleId_fixed}")