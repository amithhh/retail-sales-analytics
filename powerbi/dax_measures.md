# DAX measures for the Power BI report

Load `data/clean_orders.csv` as table `orders` (set `order_date` to Date type), then add a Date table:

```
Date = CALENDAR(MIN(orders[order_date]), MAX(orders[order_date]))
```
Relate `Date[Date]` to `orders[order_date]`.

```
Revenue = SUM(orders[sales])
Profit = SUM(orders[profit])
Profit Margin % = DIVIDE([Profit], [Revenue])
Orders = DISTINCTCOUNT(orders[order_id])
Customers = DISTINCTCOUNT(orders[customer_id])
Avg Order Value = DIVIDE([Revenue], [Orders])
Revenue LY = CALCULATE([Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
Revenue YoY % = DIVIDE([Revenue] - [Revenue LY], [Revenue LY])
Discounted Order Share = DIVIDE(CALCULATE([Orders], orders[discount] > 0), [Orders])
```

Suggested pages: (1) Overview: KPI cards, monthly revenue line, category and region bars.
(2) Discounts: margin by discount level, orders at 20%+ discount. (3) Customers: segment split, top customers.
