from datetime import datetime

from tests.helpers import make_mandate, make_request


def post(client, req):
    return client.post("/evaluate", json=req.model_dump(mode="json")).json()


def test_clean_purchase_approves(client):
    r = post(client, make_request("t1", "ThinkPad X1", "electronics", 900))
    assert r["decision"] == "approve"


def test_over_price_limit_asks_reauth(client):
    r = post(client, make_request("t2", "MacBook Pro", "electronics", 1400))
    assert r["decision"] == "reauth"


def test_wrong_category_asks_reauth(client):
    m = make_mandate("m-cat", allowed_categories=["electronics"])
    r = post(client, make_request("t3", "Running shoes", "footwear", 80, mandate=m))
    assert r["decision"] == "reauth"


def test_expired_mandate_asks_reauth(client):
    m = make_mandate("m-exp", expires_at=datetime(2026, 11, 1))
    r = post(client, make_request("t4", "ThinkPad X1", "electronics", 900, mandate=m))
    assert r["decision"] == "reauth"


def test_usual_body_wash_order_approves(client):
    r = post(client, make_request("t5", "Body wash", "toiletries", 20, qty=4))
    assert r["decision"] == "approve"


def test_quantity_spike_asks_reauth(client):
    r = post(client, make_request("t6", "Body wash", "toiletries", 40, qty=8))
    assert r["decision"] == "reauth"


def test_quantity_drop_asks_reauth(client):
    r = post(client, make_request("t7", "Body wash", "toiletries", 5, qty=1))
    assert r["decision"] == "reauth"


def test_second_body_wash_order_in_a_month_asks_reauth(client):
    first = post(client, make_request("t8a", "Body wash", "toiletries", 20, qty=4))
    second = post(client, make_request("t8b", "Body wash", "toiletries", 20, qty=4))
    assert first["decision"] == "approve"
    assert second["decision"] == "reauth"


def test_weekly_perishable_approves(client):
    r = post(client, make_request("t9", "Milk", "groceries", 6, qty=2, perishable=True))
    assert r["decision"] == "approve"


def test_total_budget_is_enforced(client):
    m = make_mandate("m-budget", total_budget=10, allowed_categories=["groceries"])
    first = post(client, make_request("t10a", "Milk", "groceries", 6, qty=2, perishable=True, mandate=m))
    second = post(client, make_request("t10b", "Milk", "groceries", 6, qty=2, perishable=True, mandate=m))
    assert first["decision"] == "approve"
    assert second["decision"] == "reauth"


def test_too_many_failed_attempts_blocks(client):
    m = make_mandate("m-attempts")
    results = [
        post(client, make_request(f"t11-{i}", "MacBook Pro", "electronics", 1400, mandate=m))["decision"]
        for i in range(4)
    ]
    assert results == ["reauth", "reauth", "reauth", "block"]