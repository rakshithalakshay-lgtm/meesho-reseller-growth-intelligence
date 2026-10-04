# Reusable Prompt Pack

## Trigger
Start when a category's `is_flagged` result is exactly `flagged`.

## Input list
- `{category}` — category name.
- `{previous_revenue}` — verified revenue for the previous month.
- `{current_revenue}` — verified revenue for the current month.
- `{mom_pct}` — verified Month-on-Month percentage from `mom_growth()`.
- `{month}` — current month.
- `{prev_month}` — previous month.

## Prompt

Using only the supplied placeholders, draft a concise stakeholder update for a regional manager using **Context → Insight → Implication**.

1. **Context:** State the category and the comparison period `{prev_month}` to `{month}`.
2. **Insight:** State the exact supplied `{mom_pct}` and label the statement **FACT**.
3. **Implication:** Give one specific, actionable next step. If a cause is proposed but is not proven by the supplied data, label it **HYPOTHESIS**.
4. Never invent or calculate an additional business number. No number may appear unless it is one of the supplied numeric placeholders.
5. Keep the language business-facing rather than implementation-facing.
6. If a reseller is ever referenced, use its coded alias only; never expose a raw reseller name.

## Checklist

Before the draft is released for human approval, verify:

- [ ] Every numeric figure in the draft matches a supplied placeholder exactly.
- [ ] The Context identifies the correct category and comparison period.
- [ ] The key numeric insight is explicitly labeled **FACT**.
- [ ] Any unproven causal explanation is explicitly labeled **HYPOTHESIS**.
- [ ] The recommendation is specific and actionable rather than vague.
- [ ] Any reseller reference uses a coded alias and contains no raw reseller name.
