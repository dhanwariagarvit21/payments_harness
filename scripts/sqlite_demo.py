import sqlite3

conn = sqlite3.connect("demo.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    item TEXT,
    category TEXT,
    price REAL,
    ts TEXT
)""")

cur.execute(
    "INSERT INTO purchases (user_id, item, category, price, ts) VALUES (?, ?, ?, ?, ?)",
    ("u1", "laptop", "electronics", 900.0, "2026-11-10"),
)
conn.commit()
rows = cur.execute(
    "SELECT * FROM purchases WHERE user_id = ? AND price > ?",
    ("u1", 500),
).fetchall()
print(rows)
conn.close()