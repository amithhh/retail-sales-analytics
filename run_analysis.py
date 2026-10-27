import re, sqlite3, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
con = sqlite3.connect("retail.db")
blocks = re.split(r"-- name: (\w+)\n", open("sql/queries.sql").read())[1:]
res = {}
for name, q in zip(blocks[0::2], blocks[1::2]):
    res[name] = pd.read_sql(q, con); print(f"\n== {name} ==\n", res[name].to_string(index=False))
    if name in ("monthly_revenue", "category_performance", "region_performance", "discount_vs_margin"):
        res[name].to_csv(f"powerbi/{name}.csv", index=False)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
m = res["monthly_revenue"]; ax[0].plot(m["month"], m["revenue"]/1e6); ax[0].set_title("Monthly revenue (₹ million)")
ax[0].set_xticks(range(0, len(m), 3)); ax[0].set_xticklabels(m["month"][::3], rotation=45)
c = res["category_performance"]; ax[1].bar(c["category"], c["margin_pct"], color="#2a9d8f"); ax[1].set_title("Profit margin % by category")
d = res["discount_vs_margin"]; ax[2].bar(d["discount_pct"].astype(int).astype(str)+"%", d["margin_pct"], color="#e76f51"); ax[2].set_title("Margin % by discount level")
plt.tight_layout(); plt.savefig("charts/overview.png", dpi=120)
