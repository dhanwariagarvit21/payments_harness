from datetime import datetime

import httpx
from rich.console import Console

from harness.schemas import Mandate, PurchaseRequest

console = Console()
URL = "http://127.0.0.1:8000/evaluate"

mandate = Mandate(
    user_id="u1",
    max_per_purchase=1000,
    total_budget=2000,
    allowed_categories=["electronics"],
    expires_at=datetime(2026, 12, 31),
)


def make_request(rid, item, category, price, query="a laptop for coding"):
    return PurchaseRequest(
        request_id=rid, user_id="u1", user_query=query, item=item,
        category=category, merchant="shop.example", price=price,
        timestamp=datetime(2026, 11, 26), mandate=mandate,
    )


# (request, expected decision)
SCENARIOS = [
    (make_request("r1", "ThinkPad X1", "electronics", 900), "approve"),
    (make_request("r2", "MacBook Pro", "electronics", 1400), "reauth"),
    (make_request("r3", "Running shoes", "footwear", 80), "reauth"),
]


def main():
    for req, expected in SCENARIOS:
        resp = httpx.post(URL, json=req.model_dump(mode="json")).json()
        got = resp["decision"]
        ok = got == expected
        tag = "[green]PASS[/green]" if ok else "[red]FAIL[/red]"
        console.print(f"{tag} {req.request_id} {req.item}: expected {expected}, got {got}")


if __name__ == "__main__":
    main()