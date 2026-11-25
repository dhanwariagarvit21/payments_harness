from datetime import datetime
from harness.schemas import Mandate, PurchaseRequest

mandate = Mandate(
    user_id="u1", max_per_purchase=1000, total_budget=2000,
    allowed_categories=["electronics"], expires_at=datetime(2026, 12, 1),
)
req = PurchaseRequest(
    request_id="r1", user_id="u1", user_query="a laptop for coding",
    item="ThinkPad X1", category="electronics", merchant="shop.example",
    price=-5, timestamp=datetime(2026, 11, 26), mandate=mandate,
)
print(req.model_dump_json(indent=2))
