from datetime import datetime

from harness.schemas import Mandate, PurchaseRequest


def make_mandate(mandate_id, **overrides):
    base = dict(
        user_id="u1",
        mandate_id=mandate_id,
        max_per_purchase=1000,
        total_budget=2000,
        allowed_categories=["electronics", "toiletries", "groceries"],
        expires_at=datetime(2026, 12, 31),
    )
    base.update(overrides)
    return Mandate(**base)


def make_request(rid, item, category, price, qty=1, perishable=False, mandate=None):
    return PurchaseRequest(
        request_id=rid, user_id="u1", user_query="a laptop for coding",
        item=item, category=category, merchant="shop.example", price=price,
        quantity=qty, perishable=perishable,
        timestamp=datetime(2026, 11, 26),
        mandate=mandate or make_mandate(f"m-{rid}"),
    )