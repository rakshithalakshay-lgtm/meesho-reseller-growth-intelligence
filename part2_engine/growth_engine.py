import csv
from typing import List, Tuple


def mom_growth(previous: float, current: float) -> float:
    """Return Month-on-Month growth percentage rounded to 2 decimals."""
    if previous == 0:
        raise ValueError("previous revenue must not be zero")
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Classify growth using the required three-state threshold rule."""
    magnitude = abs(mom_pct)
    if magnitude > threshold:
        return "flagged"
    if magnitude < threshold:
        return "not_flagged"
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> Tuple[bool, List[str]]:
    """Validate month/category/revenue/n_orders feed and preserve row error order."""
    errors: List[str] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"month", "category", "revenue", "n_orders"}
        if not required.issubset(reader.fieldnames or []):
            missing = sorted(required - set(reader.fieldnames or []))
            return False, [f"missing required columns: {', '.join(missing)}"]

        for line_no, row in enumerate(reader, start=2):
            category = (row.get("category") or "").strip()
            month = row.get("month") or ""
            revenue_raw = row.get("revenue")

            if not category:
                errors.append(f"line {line_no}: missing category (month={month})")
            if revenue_raw is None or revenue_raw.strip() == "":
                errors.append(f"line {line_no}: missing revenue (category={category})")
                continue
            try:
                revenue = float(revenue_raw)
            except ValueError:
                errors.append(f"line {line_no}: revenue not numeric: {revenue_raw!r}")
                continue
            if revenue < 0:
                errors.append(
                    f"line {line_no}: negative revenue ({revenue}) for category={category}"
                )

    return (True, []) if not errors else (False, errors)
