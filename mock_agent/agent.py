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
    allowed_categories=["electronics", "toiletries", "groceries"],
    expires_at=datetime(2026, 12, 31),
)

def make_request(rid, item, category, price, qty=1, perishable=False,
                 query="a laptop for coding", m=None):
    used = m or mandate.model_copy(update={"mandate_id": f"m-{rid}"})
    return PurchaseRequest(
        request_id=rid, user_id="u1", user_query=query, item=item,
        category=category, merchant="shop.example", price=price,
        quantity=qty, perishable=perishable,
        timestamp=datetime(2026, 11, 26), mandate=used,
    )
expired_mandate = Mandate(
    user_id="u1", max_per_purchase=1000, total_budget=2000,
    allowed_categories=["electronics"], expires_at=datetime(2026, 11, 1),
)
budget_mandate = Mandate(
    user_id="u1", mandate_id="mB", max_per_purchase=1000, total_budget=10,
    allowed_categories=["groceries"], expires_at=datetime(2026, 12, 31),
)
attempts_mandate = mandate.model_copy(update={"mandate_id": "mA"})

# (request, expected decision)
SCENARIOS = [
    (make_request("r1", "ThinkPad X1", "electronics", 900), "approve"),
    (make_request("r2", "MacBook Pro", "electronics", 1400), "reauth"),
    (make_request("r3", "Running shoes", "footwear", 80), "reauth"),
    (make_request("r4", "ThinkPad X1", "electronics", 900, m=expired_mandate), "reauth"),
    (make_request("r5", "Body wash", "toiletries", 20, qty=4), "approve"),
    (make_request("r6", "Body wash", "toiletries", 40, qty=8), "reauth"),  
    (make_request("r7", "Body wash", "toiletries", 5, qty=1), "reauth"),   
    (make_request("r8", "Body wash", "toiletries", 20, qty=4), "reauth"),
    (make_request("r9", "Milk", "groceries", 6, qty=2, perishable=True), "approve"),
    (make_request("r10", "Milk", "groceries", 6, qty=2, perishable=True, m=budget_mandate), "approve"),
    (make_request("r11", "Milk", "groceries", 6, qty=2, perishable=True, m=budget_mandate), "reauth"),
    (make_request("r12", "MacBook Pro", "electronics", 1400, m=attempts_mandate), "reauth"),
    (make_request("r13", "MacBook Pro", "electronics", 1400, m=attempts_mandate), "reauth"),
    (make_request("r14", "MacBook Pro", "electronics", 1400, m=attempts_mandate), "reauth"),
    (make_request("r15", "MacBook Pro", "electronics", 1400, m=attempts_mandate), "block"),
]


def main():
    passed = 0
    failed = 0

    console.print(f"Running {len(SCENARIOS)} test scenarios")

    try:
        for req, expected in SCENARIOS:
            response = httpx.post(URL, json=req.model_dump(mode="json"), timeout=5.0)
            response.raise_for_status()
            got = response.json()["decision"]
            ok = got == expected

            if ok:
                passed += 1
                tag = "[green]PASS[/green]"
            else:
                failed += 1
                tag = "[red]FAIL[/red]"

            console.print(f"{tag} {req.request_id} {req.item}: expected {expected}, got {got}")

        console.print(f"Summary: {passed} passed, {failed} failed, {len(SCENARIOS)} total")
    except httpx.ConnectError:
        console.print("[red]ERROR:[/red] Could not connect to the payments harness.")
        console.print("Start the server in another terminal with:")
        console.print("[bold].\\.venv\\Scripts\\python.exe -m uvicorn harness.main:app --reload[/bold]")
        raise SystemExit(1)
    except httpx.HTTPStatusError as exc:
        console.print(f"[red]ERROR:[/red] Server returned HTTP {exc.response.status_code}.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()