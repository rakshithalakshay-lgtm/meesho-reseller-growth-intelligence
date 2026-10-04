import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from part4_agent.mock_agent_runner import run

OUT = ROOT / "part1_sql" / "output"
FIX = ROOT / "part2_engine" / "fixtures"
APRIL = OUT / "monthly_category_revenue.csv"
# Build month-specific files from the full Part 1 output for scenario testing.


def _month_csv(month: str, filename: str) -> Path:
    source = APRIL
    destination = FIX / filename
    with source.open(encoding="utf-8") as f:
        lines = f.readlines()
    header = lines[0]
    selected = [line for line in lines[1:] if line.split(",", 1)[0] == month]
    destination.write_text(header + "".join(selected), encoding="utf-8")
    return destination


def test_may_scenario():
    april = _month_csv("April", "april.csv")
    may = _month_csv("May", "may.csv")
    result = run("May", str(april), str(may))
    assert result["validation_status"] == "valid"
    assert [(x["category"], x["mom_pct"], x["drafted"]) for x in result["flagged_categories"]] == [
        ("Ethnic Wear", 77.1, True),
        ("Western Wear", -23.6, True),
        ("Kids Wear", -23.48, True),
    ]
    assert set(result["suppressed_categories"]) == {"Beauty & Personal Care", "Home & Kitchen"}
    assert result["escalated_categories"] == []


def test_june_scenario():
    may = _month_csv("May", "may.csv")
    june = _month_csv("June", "june.csv")
    result = run("June", str(may), str(june))
    assert [(x["category"], x["mom_pct"]) for x in result["flagged_categories"]] == [
        ("Ethnic Wear", -58.74),
        ("Home & Kitchen", 42.59),
        ("Kids Wear", 23.9),
    ]
    assert result["suppressed_categories"] == ["Western Wear"]
    assert "Beauty & Personal Care" not in result["suppressed_categories"]
    assert result["escalated_categories"] == []


def test_corrupted_hard_stop():
    april = _month_csv("April", "april.csv")
    result = run("July", str(april), str(FIX / "corrupted_feed.csv"))
    assert result["validation_status"] == "invalid"
    assert result["action_taken"] == "hard_stop"
    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == []


def test_exact_boundary_is_escalated():
    with TemporaryDirectory() as tmp:
        previous = Path(tmp) / "boundary_previous.csv"
        current = Path(tmp) / "boundary_current.csv"
        previous.write_text("month,category,revenue,n_orders\nJuly,Test Category,100000,1\n", encoding="utf-8")
        current.write_text("month,category,revenue,n_orders\nAugust,Test Category,108000,1\n", encoding="utf-8")
        result = run("August", str(previous), str(current))
    assert result["flagged_categories"] == []
    assert result["suppressed_categories"] == []
    assert result["escalated_categories"] == ["Test Category"]


if __name__ == "__main__":
    for fn in [test_may_scenario, test_june_scenario, test_corrupted_hard_stop, test_exact_boundary_is_escalated]:
        fn()
        print(f"PASS {fn.__name__}")
