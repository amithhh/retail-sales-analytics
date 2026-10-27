"""Generates a SYNTHETIC retail orders dataset (seeded, reproducible).
Deliberately messy: duplicate rows, mixed-case regions, missing values, inconsistent dates."""
import numpy as np, pandas as pd
rng = np.random.default_rng(7)
N = 12000
cats = {"Technology": [("Laptop", 55000), ("Phone", 28000), ("Headphones", 3500), ("Smartwatch", 9000)],
        "Furniture": [("Office Chair", 7500), ("Desk", 12000), ("Bookshelf", 6000)],
        "Office Supplies": [("Notebook", 150), ("Printer Paper", 450), ("Pen Set", 250), ("Stapler", 300)]}
products = [(c, p, price) for c, ps in cats.items() for p, price in ps]
regions = {"South": ["Bangalore", "Chennai", "Kochi", "Hyderabad"], "West": ["Mumbai", "Pune", "Ahmedabad"],
           "North": ["Delhi", "Jaipur", "Lucknow"], "East": ["Kolkata", "Bhubaneswar"]}
cities = [(r, c) for r, cs in regions.items() for c in cs]
segments = ["Consumer", "Corporate", "Home Office"]
n_cust = 2500
cust_seg = rng.choice(segments, n_cust, p=[.55, .30, .15])
# a minority of customers place most orders
w = rng.pareto(1.6, n_cust) + 1; w /= w.sum()
cid = rng.choice(n_cust, N, p=w)
dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(rng.integers(0, 730, N), unit="D")
season = 1 + 0.35 * np.isin(dates.month, [10, 11, 12])   # festive-season lift
keep = rng.random(N) < (season / season.max())
dates = dates[keep]; cid = cid[keep]; n = len(dates)
pi = rng.integers(0, len(products), n); ci = rng.integers(0, len(cities), n)
qty = rng.integers(1, 5, n)
disc = rng.choice([0, 0.05, 0.10, 0.20, 0.30], n, p=[.45, .2, .15, .13, .07])
price = np.array([products[i][2] for i in pi]) * rng.uniform(0.95, 1.05, n)
sales = price * qty * (1 - disc)
margin = np.array([{"Technology": .16, "Furniture": .12, "Office Supplies": .30}[products[i][0]] for i in pi]) - disc * 0.9
profit = sales * margin
df = pd.DataFrame({"order_id": [f"ORD-{100000+i}" for i in range(n)],
    "order_date": dates, "customer_id": [f"C{c:04d}" for c in cid],
    "segment": cust_seg[cid], "region": [cities[i][0] for i in ci], "city": [cities[i][1] for i in ci],
    "category": [products[i][0] for i in pi], "product": [products[i][1] for i in pi],
    "quantity": qty, "discount": disc, "sales": sales.round(2), "profit": profit.round(2)})
df = df.sort_values("order_date").reset_index(drop=True)
# inject mess
m = df.copy()
m["region"] = m["region"].where(rng.random(n) > .04, m["region"].str.upper())
m.loc[rng.random(n) < .02, "city"] = None
m.loc[rng.random(n) < .01, "sales"] = None
m["order_date"] = m["order_date"].dt.strftime("%Y-%m-%d")
idx = rng.random(n) < .03
m.loc[idx, "order_date"] = pd.to_datetime(m.loc[idx, "order_date"]).dt.strftime("%d/%m/%Y")
m = pd.concat([m, m.sample(int(n * .015), random_state=1)]).sample(frac=1, random_state=2)
m.to_csv("data/raw_orders.csv", index=False)
print("raw rows:", len(m))
