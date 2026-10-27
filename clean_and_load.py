"""Clean raw_orders.csv with pandas and load it into a SQLite database (ANSI SQL, MySQL-portable)."""
import pandas as pd, sqlite3
df = pd.read_csv("data/raw_orders.csv")
print("raw rows:", len(df))
df = df.drop_duplicates(subset="order_id")
print("after dropping duplicate order_ids:", len(df))
def parse(s):
    return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce").fillna(pd.to_datetime(s, format="%d/%m/%Y", errors="coerce"))
df["order_date"] = parse(df["order_date"])
df["region"] = df["region"].str.title()
df["city"] = df["city"].fillna("Unknown")
missing_sales = df["sales"].isna().sum()
# Sales is quantity-driven; rows with no sales value cannot be repaired reliably, so drop them
df = df.dropna(subset=["sales"])
print(f"dropped {missing_sales} rows with missing sales; clean rows: {len(df)}")
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
con = sqlite3.connect("retail.db")
df.to_sql("orders", con, if_exists="replace", index=False)
con.close()
df.to_csv("data/clean_orders.csv", index=False)
