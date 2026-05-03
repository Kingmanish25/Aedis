import sqlite3
import random
import datetime

conn = sqlite3.connect("data/finance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    region TEXT,
    product TEXT,
    revenue REAL,
    cost REAL,
    profit REAL,
    customer_id INTEGER
)
""")

regions = ["North", "South", "East", "West"]
products = ["A", "B", "C", "D"]

for i in range(2000):
    date = datetime.date(2023, random.randint(1,12), random.randint(1,28))
    region = random.choice(regions)
    product = random.choice(products)

    revenue = random.randint(1000, 10000)

    if date.month in [4,5,6]:
        revenue *= 0.6

    cost = revenue * random.uniform(0.5, 0.8)
    profit = revenue - cost

    cur.execute("""
    INSERT INTO sales (date, region, product, revenue, cost, profit, customer_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (str(date), region, product, revenue, cost, profit, random.randint(1,100)))

conn.commit()
conn.close()