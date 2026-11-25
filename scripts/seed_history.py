from harness import db

db.init_db(reset=True)

# (item, category, quantity, perishable, price, date)
history = [
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
for item, cat, qty, per, price, ts in history:
    db.insert_purchase("u1", item, cat, qty, per, price, ts)

print(f"seeded {len(history)} purchases for u1")