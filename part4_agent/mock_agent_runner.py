import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed
from part3_narrative.narrative_engine import render_flagged_narrative


def _read_revenue_by_category(csv_path: str) -> Dict[str, Dict[str, str]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return {row["category"]: row for row in csv.DictReader(f)}


def _hard_stop(month: str, errors: List[str]) -> dict:
    return {
        "run_month": month,
        "validation_status": "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "hard_stop",
    }


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Run the guarded monthly workflow and return the exact seven-key JSON shape."""
    # 1-2. Validate current feed before any MoM calculation.
    current_valid, current_errors = validate_feed(current_month_csv)
    if not current_valid:
        return _hard_stop(month, current_errors)

    # Previous feed is also an input and must be valid before comparison.
    previous_valid, previous_errors = validate_feed(previous_month_csv)
    if not previous_valid:
        return _hard_stop(month, previous_errors)

    previous = _read_revenue_by_category(previous_month_csv)
    current = _read_revenue_by_category(current_month_csv)

    # 3-4. Compute and classify every current category.
    classifications = []
    escalated = []
    for category, current_row in current.items():
        if category not in previous:
            continue
        previous_revenue = float(previous[category]["revenue"])
        current_revenue = float(current_row["revenue"])
        pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(pct)
        item = {
            "category": category,
            "mom_pct": pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
            "status": status,
        }
        if status == "escalate_exact_boundary":
            escalated.append(category)
        elif status == "flagged":
            classifications.append(item)

    # 5. Sort flagged categories by magnitude.
    classifications.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # 6-7. Draft only top 3; explicitly suppress the remainder.
    top_three = classifications[:3]
    remaining = classifications[3:]
    flagged_categories = []
    for item in top_three:
        current_row = current[item["category"]]
        previous_month = previous[item["category"]]["month"]
        message = render_flagged_narrative(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=current_row["month"],
            prev_month=previous_month,
        ).strip()
        flagged_categories.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": message,
        })

    suppressed_categories = [item["category"] for item in remaining]

    # 8. Emit exactly the required top-level schema.
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_categories,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


def _main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: python part4_agent/mock_agent_runner.py <month> <previous_csv> <current_csv>"
        )
    month, previous_csv, current_csv = sys.argv[1:]
    print(json.dumps(run(month, previous_csv, current_csv), indent=2))


if __name__ == "__main__":
    _main()
