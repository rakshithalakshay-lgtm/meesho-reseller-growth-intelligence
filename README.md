# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end monthly reseller monitoring pipeline built for the IIT Hub capstone project.

**Pipeline:** SQL → Python Guardrails → Reliable Narrative → Agent Workflow → Human Approval

## Business problem

The pipeline replaces a manual monthly monitoring process with a repeatable workflow that:

- calculates verified category and regional business numbers;
- turns “significant change” into a testable 8% MoM rule;
- validates bad input before calculations run;
- drafts stakeholder-ready narratives without inventing figures;
- masks raw reseller names in external-facing narratives; and
- limits notifications to the top three flagged categories while holding all drafts for human approval.

## Repository structure

```text
README.md
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db
part1_sql/
├── queries.sql
├── run_queries.py
└── output/
    ├── monthly_category_revenue.csv
    ├── region_revenue.csv
    ├── top_resellers.csv
    ├── zero_order_resellers.csv
    ├── zero_order_count_comparison.csv
    ├── june_delivered_aov.csv
    └── README.md
part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/
    ├── corrupted_feed.csv
    └── monthly_category_revenue.csv
part3_narrative/
├── prompt_pack.md
├── narrative_report.md
├── narrative_engine.py
├── masking.py
└── test_masking.py
part4_agent/
├── agent_spec.md
├── mock_agent_runner.py
└── test_mock_agent_runner.py
```

## Requirements

- Python 3.9+ recommended.
- No third-party Python packages are required.
- SQLite is provided by Python's standard-library `sqlite3` module.
- No API key, paid service, hosted service, or network connection is required.

The entire pipeline is designed to pass with **zero API keys set**.

## 1. Generate the seeded dataset

Do not change the seed, row counts, status weights, or category weights. The acceptance criteria are based on the supplied deterministic script.

From the repository root:

```bash
python data/generate_dataset.py
```

Expected result:

- 24 resellers
- 900 orders
- 300 orders each for April, May, and June 2026
- `data/resellers.csv`
- `data/orders.csv`
- `data/meesho_reseller.db`

## 2. Run Part 1 — SQL Business Query Engine

Run:

```bash
python part1_sql/run_queries.py
```

The SQL logic is documented in `part1_sql/queries.sql`. The runner executes the same SQL against SQLite and writes the required CSV outputs under `part1_sql/output/`.

The key hand-off file is:

```text
part1_sql/output/monthly_category_revenue.csv
```

It has exactly these columns:

```text
month,category,revenue,n_orders
```

The five required questions are:

1. Monthly revenue by category.
2. Region-wise revenue and order count.
3. Top five resellers by spend above INR 50000.
4. Resellers with zero orders, including the `COUNT(*)` vs `COUNT(order_id)` demonstration.
5. June Delivered AOV.

## 3. Run Part 2 — Python Guardrail & Growth Engine

Run the standard-library test file directly:

```bash
python part2_engine/test_growth_engine.py
```

The engine contains exactly the required core functions:

- `mom_growth(previous, current)`
- `is_flagged(mom_pct, threshold=8.0)`
- `validate_feed(csv_path)`

The threshold has three states:

- absolute MoM > 8% → `flagged`
- absolute MoM < 8% → `not_flagged`
- absolute MoM = 8% → `escalate_exact_boundary`

The corrupted fixture must produce exactly three validation errors in row order, and the validated Part 1 feed must return `(True, [])`.

## 4. Run Part 3 — Reliable AI Narrative

No real LLM is needed. The project uses deterministic template filling in `narrative_engine.py`.

The reusable prompt pack is in:

```text
part3_narrative/prompt_pack.md
```

The worked narrative and chart-choice justifications are in:

```text
part3_narrative/narrative_report.md
```

Run the masking tests:

```bash
cd part3_narrative
python test_masking.py
cd ..
```

The masking policy converts, for example, `RS019` to `ALIAS-19` and rejects narratives containing raw reseller names.

## 5. Run Part 4 — Agentic Workflow + Mock Runner

The agent runner imports the Part 2 functions **unmodified** and reuses the Part 3 narrative template-fill function.

Example May run:

```bash
python part4_agent/mock_agent_runner.py May \
  part2_engine/fixtures/april.csv \
  part2_engine/fixtures/may.csv
```

Example June run:

```bash
python part4_agent/mock_agent_runner.py June \
  part2_engine/fixtures/may2.csv \
  part2_engine/fixtures/june.csv
```

For repeatable scenario tests, run:

```bash
python part4_agent/test_mock_agent_runner.py
```

The runner follows the required order:

1. Validate feed.
2. Hard Stop if invalid.
3. Calculate MoM for each category.
4. Apply the three-state flag rule.
5. Sort flagged categories by absolute MoM magnitude.
6. Draft at most the top three.
7. Suppress remaining flagged categories and separately record exact-boundary escalations.
8. Emit one structured JSON object.

## Expected acceptance results

### May: April → May

Drafted, in order:

1. Ethnic Wear — 77.1%
2. Western Wear — -23.6%
3. Kids Wear — -23.48%

Suppressed:

- Beauty & Personal Care
- Home & Kitchen

### June: May → June

Drafted, in order:

1. Ethnic Wear — -58.74%
2. Home & Kitchen — 42.59%
3. Kids Wear — 23.9%

Suppressed:

- Western Wear — 11.97%

Beauty & Personal Care at 5.67% is `not_flagged`, so it appears in neither flagged nor suppressed lists.

### Corrupted feed

The run must become:

```text
validation_status = invalid
action_taken = hard_stop
```

with the three required validation errors and no MoM calculations or drafts.

## How the Parts connect

**Part 1 → Part 2:** SQL computes the real business numbers first. The monthly category CSV is handed directly to the Python validation and growth engine.

**Part 2 → Part 3:** Verified MoM and flag results provide the trusted inputs to the deterministic narrative template.

**Part 2 + Part 3 → Part 4:** The agent imports the Part 2 functions without re-implementing their math and uses the Part 3 template-fill logic to create held drafts.

**Part 4 → Human:** The agent never sends a message. It returns a structured result with drafts held for human approval.

This maps to the workflow patterns described in the brief: **compute real numbers → hand off → draft → validate**, and **Intake → Summary → Report Draft → Validate**.

## Testing checklist before GitHub submission

- [ ] Dataset regenerated from the exact supplied script.
- [ ] 24 resellers and 900 orders confirmed.
- [ ] All five SQL questions match the acceptance values.
- [ ] Part 2 three functions implemented.
- [ ] Four required Given-When-Then cases pass.
- [ ] Corrupted feed produces exactly three errors in order.
- [ ] Valid Part 1 feed passes validation.
- [ ] May and June MoM tables match the acceptance values.
- [ ] Prompt pack has Trigger, Input list, Prompt, and Checklist.
- [ ] May and June narratives contain exact values and FACT/HYPOTHESIS labels.
- [ ] Chart-choice section answers all three questions without images.
- [ ] Masking positive and negative tests pass.
- [ ] Agent spec documents all five components and guardrails.
- [ ] May, June, corrupted-feed, and exact-boundary agent tests pass.
- [ ] JSON has exactly the required seven top-level keys.
- [ ] No API key or paid service is required.
- [ ] No raw reseller names appear in external-facing narrative.
- [ ] No automatic sending exists.

## Academic integrity / documentation

The implementation uses Python standard-library modules (`csv`, `sqlite3`, `pathlib`, `json`, and `typing`) and follows the project brief's allowance to consult official Python standard-library documentation. No external API or paid service is used.

## Submission

Create **one public GitHub repository** containing this project and submit **only the repository link**. Do not submit a ZIP, Google Drive link, screenshots, PDF, presentation, or other separate deliverable.
