# Reliable AI Narrative Report

## Worked Narrative 1 — May Ethnic Wear

### Context
Ethnic Wear revenue is being compared for May 2026 versus April 2026.

### Insight
Ethnic Wear revenue increased by **77.1% MoM — FACT**.

### Implication
Review the May promotional calendar, category-level order mix, and regional execution to identify the operational drivers behind the movement and determine whether any successful activity should be repeated — **HYPOTHESIS**, not proven by the revenue feed alone.

### Self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, May 2026, April 2026, and the exact 77.1% result.
- **Audience fit:** Pass — the wording focuses on what a regional manager should understand and investigate rather than on implementation details.
- **Completeness:** Pass — Context, Insight, and Implication are all present.
- **Actionability:** Pass — it names concrete areas to review rather than simply saying to investigate the category.

## Worked Narrative 2 — June Ethnic Wear

### Context
Ethnic Wear revenue is being compared for June 2026 versus May 2026.

### Insight
Ethnic Wear revenue decreased by **58.74% MoM — FACT**.

### Implication
Review the June promotional calendar, availability or assortment changes, and regional execution to determine which operational change should be addressed first — **HYPOTHESIS**, not proven by the revenue feed alone.

### Self-score
- **Specificity:** Pass — the narrative names Ethnic Wear, June 2026, May 2026, and the exact -58.74% result.
- **Audience fit:** Pass — the message is written for a regional manager who needs a decision-oriented summary.
- **Completeness:** Pass — Context, Insight, and Implication are all present.
- **Actionability:** Pass — it specifies the operational areas to review and prioritize.

## Top-reseller narrative with masking

The five high-spend resellers are referenced only by region and coded alias in any external-facing summary:

- West — ALIAS-19
- West — ALIAS-22
- South — ALIAS-12
- North — ALIAS-06
- North — ALIAS-05

**FACT:** These are the five reseller IDs returned by the Part 1 `HAVING total_spend > 50000` query, represented externally by coded aliases rather than raw reseller names.

**HYPOTHESIS:** A regional manager can use the aliases to investigate performance internally without exposing raw reseller identities in an external-facing narrative.

## Chart-choice justification

### 1. Which month had the highest total revenue?
Use a **column chart**. This is a univariate comparison of total revenue across months, so one quantitative measure is compared across one categorical dimension. The message should be clear within 10 seconds; the y-axis should start at zero to avoid visually exaggerating differences; no 3D treatment is needed; and no legend is necessary because there is only one series. May is the highest month at INR 444594.25.

### 2. What percentage share does Ethnic Wear represent of April's total revenue?
Use a **100% stacked bar** with Ethnic Wear and the remainder, because the question is a part-to-whole comparison. This keeps the 24.92% share visually simple and readable within 10 seconds. The scale should start at zero, 3D should be avoided, and a legend is useful only if the two components are represented as separate series.

### 3. How do the four regions compare on total revenue?
Use a **horizontal bar chart**. This is a univariate comparison of one quantitative measure across four categorical regions. A zero-starting axis makes the differences trustworthy and the horizontal layout keeps region names easy to read. The message should be clear within 10 seconds; avoid 3D; and no legend is needed because there is one revenue series.
