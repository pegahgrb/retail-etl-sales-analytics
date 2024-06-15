-- Total sales by branch
SELECT
    b.branch_name,
    ROUND(SUM(f.sales_amount), 2) AS total_sales
FROM fact_sales f
JOIN dim_branch b ON f.branch_key = b.branch_key
GROUP BY b.branch_name
ORDER BY total_sales DESC;

-- Total sales by category
SELECT
    p.category,
    ROUND(SUM(f.sales_amount), 2) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_sales DESC;

-- Top products by revenue
SELECT
    p.product_name,
    ROUND(SUM(f.sales_amount), 2) AS total_sales
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY total_sales DESC
LIMIT 5;

