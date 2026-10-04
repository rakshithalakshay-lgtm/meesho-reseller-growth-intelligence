from pathlib import Path

from growth_engine import is_flagged, mom_growth, validate_feed

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_april_may_ethnic_wear():
    # GIVEN April -> May Ethnic Wear revenue
    # WHEN MoM growth and flag are calculated
    # THEN exact expected values are returned
    pct = mom_growth(104520.77, 185107.61)
    assert pct == 77.1
    assert is_flagged(pct) == "flagged"


def test_may_june_beauty():
    pct = mom_growth(35542.11, 37559.07)
    assert pct == 5.67
    assert is_flagged(pct) == "not_flagged"


def test_exact_boundary():
    pct = mom_growth(100000, 108000)
    assert pct == 8.0
    assert is_flagged(pct) == "escalate_exact_boundary"


def test_corrupted_feed_exact_errors():
    valid, errors = validate_feed(str(FIXTURES / "corrupted_feed.csv"))
    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_part1_feed():
    valid, errors = validate_feed(str(FIXTURES / "monthly_category_revenue.csv"))
    assert valid is True
    assert errors == []


def test_may_all_categories():
    expected = {
        "Ethnic Wear": (77.1, "flagged"),
        "Western Wear": (-23.6, "flagged"),
        "Kids Wear": (-23.48, "flagged"),
        "Home & Kitchen": (-9.25, "flagged"),
        "Beauty & Personal Care": (-12.75, "flagged"),
    }
    for category, (previous, current) in {
        "Ethnic Wear": (104520.77, 185107.61),
        "Western Wear": (113866.15, 86998.18),
        "Kids Wear": (59847.27, 45793.78),
        "Home & Kitchen": (100446.23, 91152.57),
        "Beauty & Personal Care": (40737.01, 35542.11),
    }.items():
        pct = mom_growth(previous, current)
        assert (pct, is_flagged(pct)) == expected[category]


def test_june_all_categories():
    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }
    for category, (previous, current) in {
        "Ethnic Wear": (185107.61, 76371.53),
        "Western Wear": (86998.18, 97415.64),
        "Kids Wear": (45793.78, 56737.78),
        "Home & Kitchen": (91152.57, 129971.22),
        "Beauty & Personal Care": (35542.11, 37559.07),
    }.items():
        pct = mom_growth(previous, current)
        assert (pct, is_flagged(pct)) == expected[category]


if __name__ == "__main__":
    tests = [
        test_april_may_ethnic_wear, test_may_june_beauty, test_exact_boundary,
        test_corrupted_feed_exact_errors, test_valid_part1_feed,
        test_may_all_categories, test_june_all_categories,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
