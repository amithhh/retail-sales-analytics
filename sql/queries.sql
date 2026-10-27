-- name: monthly_revenue
SELECT substr(order_date,1,7) AS month,
       ROUND(SUM(sales),0) AS revenue,
       ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),1) AS margin_pct
FROM orders GROUP BY 1 ORDER BY 1;

-- name: category_performance
SELECT category, ROUND(SUM(sales),0) AS revenue, ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),1) AS margin_pct
FROM orders GROUP BY category ORDER BY revenue DESC;

-- name: top_products
SELECT product, category, ROUND(SUM(sales),0) AS revenue, ROUND(SUM(profit),0) AS profit
FROM orders GROUP BY product, category ORDER BY revenue DESC LIMIT 10;

-- name: region_performance
SELECT region, COUNT(*) AS orders, ROUND(SUM(sales),0) AS revenue,
       ROUND(100.0*SUM(profit)/SUM(sales),1) AS margin_pct
FROM orders GROUP BY region ORDER BY revenue DESC;

-- name: discount_vs_margin
SELECT ROUND(discount*100) AS discount_pct, COUNT(*) AS orders,
       ROUND(SUM(sales),0) AS revenue, ROUND(100.0*SUM(profit)/SUM(sales),1) AS margin_pct
FROM orders GROUP BY discount ORDER BY discount;

-- name: customer_concentration
WITH cust AS (
  SELECT customer_id, SUM(sales) AS revenue FROM orders GROUP BY customer_id
), ranked AS (
  SELECT revenue, ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn, COUNT(*) OVER () AS total FROM cust
)
SELECT ROUND(100.0*SUM(CASE WHEN rn <= total*0.2 THEN revenue END)/SUM(revenue),1) AS top20pct_customers_share_of_revenue
FROM ranked;

-- name: segment_summary
SELECT segment, COUNT(DISTINCT customer_id) AS customers, ROUND(SUM(sales),0) AS revenue,
       ROUND(SUM(sales)/COUNT(DISTINCT customer_id),0) AS revenue_per_customer
FROM orders GROUP BY segment ORDER BY revenue DESC;

-- name: repeat_customers
SELECT ROUND(100.0*SUM(CASE WHEN n>1 THEN 1 ELSE 0 END)/COUNT(*),1) AS repeat_customer_pct
FROM (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id);

-- name: yoy_growth_by_quarter
WITH q AS (
  SELECT substr(order_date,1,4) AS yr,
         ((CAST(substr(order_date,6,2) AS INT)-1)/3)+1 AS qtr, SUM(sales) AS revenue
  FROM orders GROUP BY 1,2
)
SELECT a.qtr, ROUND(a.revenue,0) AS rev_2024, ROUND(b.revenue,0) AS rev_2025,
       ROUND(100.0*(b.revenue-a.revenue)/a.revenue,1) AS yoy_pct
FROM q a JOIN q b ON a.qtr=b.qtr AND a.yr='2024' AND b.yr='2025' ORDER BY a.qtr;
