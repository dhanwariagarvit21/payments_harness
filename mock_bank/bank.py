def charge(user_id: str, amount: float, request_id: str) -> dict:
    """Pretends to move money. Always succeeds for now."""
    print(f"[BANK] charged {user_id} ${amount:.2f} for {request_id}")
    return {"status": "paid", "request_id": request_id, "amount": amount}