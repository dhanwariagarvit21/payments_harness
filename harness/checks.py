from harness.schemas import PurchaseRequest, Signal
from collections import Counter
from datetime import timedelta
from harness import db

def check_price_limit(req: PurchaseRequest) -> Signal:
    limit = req.mandate.max_per_purchase
    return Signal(
        name="price_over_limit",
        triggered=req.price > limit,
        weight=1.0,
        detail=f"price {req.price} vs per-purchase limit {limit}",
    )


def check_category(req: PurchaseRequest) -> Signal:
    allowed = req.mandate.allowed_categories
    return Signal(
        name="category_not_allowed",
        triggered=req.category not in allowed,
        weight=1.0,
        detail=f"category '{req.category}' vs allowed {allowed}",
    )


def check_expiry(req: PurchaseRequest) -> Signal:
    expires = req.mandate.expires_at
    return Signal(
        name="mandate_expired",
        triggered=req.timestamp > expires,
        weight=1.0,
        detail=f"request at {req.timestamp} vs mandate expiry {expires}",
    )
def check_new_item(req: PurchaseRequest) -> Signal:
    rows = db.category_rows(req.user_id, req.category)
    if not rows:
        return Signal(name="new_category", triggered=True, weight=1.0,
                      detail=f"user has never bought anything in '{req.category}'")
    if not any(r["item"] == req.item for r in rows):
        return Signal(name="new_item", triggered=True, weight=0.5,
                      detail=f"'{req.item}' is new, but the category is familiar")
    return Signal(name="new_item", triggered=False, weight=0.0, detail="item seen before")


def _avg_quantity(rows):
    return sum(r["quantity"] for r in rows) / len(rows)


def check_quantity_spike(req: PurchaseRequest) -> Signal:
    quantity = getattr(req, "quantity", 1)
    rows = db.category_rows(req.user_id, req.category)
    if not rows:
        return Signal(name="quantity_spike", triggered=False, weight=0.0, detail="no history")
    avg = _avg_quantity(rows)
    return Signal(name="quantity_spike", triggered=quantity > 1.5 * avg, weight=1.0,
                  detail=f"quantity {quantity} vs usual {avg:.1f}")


def check_quantity_drop(req: PurchaseRequest) -> Signal:
    quantity = getattr(req, "quantity", 1)
    rows = db.category_rows(req.user_id, req.category)
    if not rows:
        return Signal(name="quantity_drop", triggered=False, weight=0.0, detail="no history")
    avg = _avg_quantity(rows)
    return Signal(name="quantity_drop", triggered=quantity < 0.5 * avg, weight=1.0,
                  detail=f"quantity {quantity} vs usual {avg:.1f}")


def check_frequency(req: PurchaseRequest) -> Signal:
    if getattr(req, "perishable", False):
        return Signal(name="purchase_frequency", triggered=False, weight=0.0,
                      detail="perishable: frequent buying is normal")
    rows = db.category_rows(req.user_id, req.category)
    if not rows:
        return Signal(name="purchase_frequency", triggered=False, weight=0.0, detail="no history")
    per_month = Counter(r["ts"][:7] for r in rows)       # purchases per month
    typical = sum(per_month.values()) / len(per_month)
    since = (req.timestamp - timedelta(days=30)).date().isoformat()
    recent = sum(1 for r in rows if r["ts"] >= since)
    return Signal(name="purchase_frequency", triggered=recent + 1 > 1.5 * typical, weight=1.0,
                  detail=f"{recent} in last 30 days, typical {typical:.1f} per month")
def check_budget(req: PurchaseRequest) -> Signal:
    mandate_id = getattr(req.mandate, "mandate_id", "default")
    spent = db.mandate_spent(mandate_id)
    total = req.mandate.total_budget
    return Signal(name="budget_exceeded", triggered=spent + req.price > total, weight=1.0,
                  detail=f"spent {spent} + this {req.price} vs budget {total}")