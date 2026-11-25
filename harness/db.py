import sqlite3

DB_PATH = "harness.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(reset: bool = False):
    conn = _connect()
    if reset:
        conn.execute("DROP TABLE IF EXISTS purchases")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,
            user_id TEXT, item TEXT, category TEXT,
            quantity INTEGER, perishable INTEGER,
            price REAL, ts TEXT
        )""")
    conn.commit()
    conn.close()


def insert_purchase(user_id, item, category, quantity, perishable, price, ts):
    conn = _connect()
    conn.execute(
        "INSERT INTO purchases (user_id, item, category, quantity, perishable, price, ts) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, item, category, quantity, int(perishable), price, ts),
    )
    conn.commit()
    conn.close()


def record_purchase(req):
    quantity = getattr(req, "quantity", 1)
    perishable = getattr(req, "perishable", False)
    insert_purchase(req.user_id, req.item, req.category, quantity,
                    perishable, req.price, req.timestamp.date().isoformat())


def category_rows(user_id, category):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM purchases WHERE user_id = ? AND category = ?",
        (user_id, category),
    ).fetchall()
    conn.close()
    return rows