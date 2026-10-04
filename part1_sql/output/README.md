# Part 1 SQL Output Notes

The five required business questions are implemented in `../queries.sql` and executed by `../run_queries.py`.

## COUNT(*) vs COUNT(order_id)

For the zero-order reseller `RS024`, the LEFT JOIN produces one unmatched row. `COUNT(*)` therefore returns `1` because the row itself exists after the LEFT JOIN. `COUNT(order_id)` returns `0` because the joined `order_id` is NULL. Therefore, `COUNT(order_id)` is the correct way to detect zero matching orders.

Expected comparison: `row_count = 1`, `order_id_count = 0`.
