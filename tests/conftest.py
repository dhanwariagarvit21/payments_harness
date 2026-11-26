import pytest
from fastapi.testclient import TestClient

from harness import db
from harness.main import app

# (item, category, quantity, perishable, price, date)
HISTORY = [
    ("Body wash", "toiletries", 4, False, 20, "2026-06-05"),
    ("Body wash", "toiletries", 4, False, 20, "2026-07-05"),
    ("Body wash", "toiletries", 4, False, 20, "2026-08-05"),
    ("Body wash", "toiletries", 4, False, 20, "2026-09-05"),
    ("Body wash", "toiletries", 4, False, 20, "2026-10-05"),
    ("ThinkPad T14", "electronics", 1, False, 850, "2026-03-10"),
    ("Milk", "groceries", 2, True, 3, "2026-11-05"),
    ("Milk", "groceries", 2, True, 3, "2026-11-12"),
    ("Milk", "groceries", 2, True, 3, "2026-11-19"),
]


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A fresh database with u1's history, different for every test."""
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db(reset=True)
    for item, cat, qty, per, price, ts in HISTORY:
        db.insert_purchase("u1", item, cat, qty, per, price, ts)
    return TestClient(app)