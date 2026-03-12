-- =====================================================
-- Superstore Data Engineering Project
-- Analytics Queries
-- =====================================================

-- 1. Overall business performance
SELECT
    SUM(sales) AS total_revenue,
    SUM(profit) AS total_profit,
    SUM(quantity) AS total_quantity
FROM fact_sales;


-- 2. Monthly revenue trend
SELECT
    EXTRACT(YEAR FROM order_date) AS year,
    EXTRACT(MONTH FROM order_date) AS month,
    SUM(sales) AS monthly_revenue
FROM fact_sales
GROUP BY
    EXTRACT(YEAR FROM order_date),
    EXTRACT(MONTH FROM order_date)
ORDER BY year, month;


-- 3. Top 10 products by revenue
SELECT
    p.product_id,
    p.product_name,
    SUM(f.sales) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_sales DESC
LIMIT 10;


-- 4. Revenue and profit by category
SELECT
    p.category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;


-- 5. Revenue and profit by region
SELECT
    l.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.region
ORDER BY total_sales DESC;


-- 6. Top 10 customers by revenue
SELECT
    c.customer_id,
    c.customer_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- 7. Average discount by category
SELECT
    p.category,
    AVG(f.discount) AS avg_discount
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_discount DESC;


-- 8. Top 10 most profitable products
SELECT
    p.product_id,
    p.product_name,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_profit DESC
LIMIT 10;