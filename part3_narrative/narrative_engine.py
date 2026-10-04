from pathlib import Path

PROMPT_TEMPLATE = """Context: {category} revenue for {month} compared with {prev_month}.

Insight: {category} revenue changed by {mom_pct}% MoM — FACT.

Implication: Review the category's operational drivers for the period and identify the most relevant next action — HYPOTHESIS until supported by additional evidence.
"""


def render_flagged_narrative(category: str, previous_revenue: float, current_revenue: float,
                              mom_pct: float, month: str, prev_month: str) -> str:
    """Deterministically fill the Part 3 narrative template from verified values."""
    return PROMPT_TEMPLATE.format(
        category=category,
        previous_revenue=previous_revenue,
        current_revenue=current_revenue,
        mom_pct=mom_pct,
        month=month,
        prev_month=prev_month,
    )


def load_prompt_pack() -> str:
    return Path(__file__).with_name("prompt_pack.md").read_text(encoding="utf-8")
