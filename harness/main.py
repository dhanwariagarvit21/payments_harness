from fastapi import FastAPI
from harness import db
from harness.engine import decide
from harness.schemas import Decision, DecisionResponse, PurchaseRequest
from mock_bank.bank import charge

app = FastAPI(title="Agentic Payments Harness")
db.init_db()

@app.post("/evaluate", response_model=DecisionResponse)
def evaluate(req: PurchaseRequest):
    mandate_id = getattr(req.mandate, "mandate_id", "default")
    result = decide(req)
    db.record_attempt(mandate_id, req.request_id, result.decision.value)
    if result.decision == Decision.APPROVE:
        charge(req.user_id, req.price, req.request_id)
        db.record_purchase(req)
        db.record_spend(mandate_id, req.request_id, req.price)
    return result