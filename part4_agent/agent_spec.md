# Agent Specification — Meesho Reseller Growth & Alert Intelligence

## Goal
Keep category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any drafted message is considered sent.

## Tools
- `validate_feed()` — Part 2 input guardrail.
- `mom_growth()` — Part 2 exact MoM calculation.
- `is_flagged()` — Part 2 three-state threshold decision.
- `render_flagged_narrative()` — Part 3 deterministic narrative template-fill function.

## Memory / State
The workflow needs the previous month's verified revenue per category so the next run can calculate MoM movement against the current month's feed. In this implementation the state is supplied as `previous_month_csv`.

## Planner
1. Load the monthly revenue feed and run `validate_feed()`.
2. If invalid, Hard Stop and report validation errors.
3. If valid, calculate `mom_growth()` for every category against the previous month.
4. Run `is_flagged()` for every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft messages for at most the top three flagged categories using the Part 3 template.
7. Put remaining flagged categories into `suppressed_categories` for manual review; keep exact-boundary cases separate in `escalated_categories`.
8. Emit one structured JSON object for the run.

## Feedback Loop
A drafted message is never automatically sent. The runner marks the run as `drafted_and_held_for_approval`; a human must approve any message before it could be considered sent. No email, SMTP, or network integration exists in this project.

## Guardrails

### Input guardrail
`validate_feed()` must pass before any MoM calculation or narrative drafting occurs. Invalid input causes an immediate Hard Stop.

### Action guardrail
No message is auto-sent. The system only drafts messages and holds them for human approval.

### Output guardrail
Every numeric value in a drafted message must trace to a verified Part 1/Part 2 value. The narrative template does not invent business figures.

## Success and Error Conditions

**Success:** the feed is valid and the run produces the correctly ranked drafts, suppressed list, and exact-boundary escalation list. A run may also correctly produce zero drafts when nothing crosses the threshold.

**Error:** `validate_feed()` returns `False`. The runner returns `validation_status = "invalid"`, `action_taken = "hard_stop"`, surfaces the errors, and produces no MoM results or drafts.

## Given–When–Then Agent Specifications

### 1. April → May Ethnic Wear
**GIVEN** April → May Ethnic Wear revenue is 104520.77 → 185107.61.  
**WHEN** the agent calculates MoM and applies the threshold rule.  
**THEN** MoM is 77.1 and the result is `flagged`.

### 2. May → June Beauty & Personal Care
**GIVEN** May → June Beauty & Personal Care revenue is 35542.11 → 37559.07.  
**WHEN** the agent calculates MoM and applies the threshold rule.  
**THEN** MoM is 5.67 and the result is `not_flagged`.

### 3. Exact 8% boundary
**GIVEN** previous revenue is 100000 and current revenue is 108000.  
**WHEN** the agent evaluates the threshold.  
**THEN** MoM is exactly 8.0 and the result is `escalate_exact_boundary`, not `flagged` or `not_flagged`.

### 4. Corrupted feed
**GIVEN** the corrupted fixture is supplied as the current feed.  
**WHEN** the agent validates the feed.  
**THEN** it returns the three required errors in order, stops immediately, performs no MoM calculation, and returns `action_taken = "hard_stop"`.

## Integration Notes
Part 4 imports the Part 2 functions directly and does not re-implement their mathematics. It reuses the Part 3 deterministic template-fill function. This keeps the pipeline integrated and makes the guardrails testable at the workflow level.
