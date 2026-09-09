"""
MCP Server for Backdoor Criterion Confounder Adjustment Skill
"""

import json
import sys
from client import BackdoorCriterionEngine

def handle_call(name: str, args: dict) -> dict:
    if name == "validate_backdoor_adjustment":
        nodes = args.get("nodes", ["C", "X", "Y"])
        edges = [tuple(e) for e in args.get("edges", [["C", "X"], ["C", "Y"], ["X", "Y"]])]
        t = args.get("treatment", "X")
        y = args.get("outcome", "Y")
        z = set(args.get("adjustment_set", ["C"]))
        engine = BackdoorCriterionEngine(nodes, edges)
        valid, explanation = engine.check_backdoor_criterion(t, y, z)
        return {"is_valid_adjustment_set": valid, "explanation": explanation}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
