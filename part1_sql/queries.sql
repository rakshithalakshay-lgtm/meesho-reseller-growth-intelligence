-- Meesho Reseller Growth & Alert Intelligence Pipeline
-- Part 1: five required business questions.

-- Q1: Monthly revenue by category
SELECT month, category,
       ROUND(SUM(quantity * unit_price), 2) AS revenue,
       COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END,
         CASE category
           WHEN 'Ethnic Wear' THEN 1
           WHEN 'Western Wear' THEN 2
           WHEN 'Kids Wear' THEN 3
           WHEN 'Home & Kitchen' THEN 4
           WHEN 'Beauty & Personal Care' THEN 5
         END;

-- Q2: Region-wise total revenue and order count
SELECT r.region,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
       COUNT(*) AS order_count
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

-- Q3: Top 5 resellers by total spend
SELECT r.reseller_id,
       r.reseller_name,
       ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

-- Q4a: Resellers who have never placed an order
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

-- Q4b: COUNT(*) vs COUNT(order_id) for RS024
-- COUNT(*) counts the unmatched LEFT JOIN row itself (1), while
-- COUNT(order_id) counts only non-NULL order IDs (0). Therefore
-- COUNT(order_id) is the correct zero-match detector.
SELECT r.reseller_id,
       COUNT(*) AS row_count,
       COUNT(o.order_id) AS order_id_count
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;

-- Q5: June AOV for Delivered orders only
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
