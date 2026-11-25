from fastapi import FastAPI

from harness.engine import decide
from harness.schemas import Decision, DecisionResponse, PurchaseRequest
from mock_bank.bank import charge

app = FastAPI(title="Agentic Payments Harness")


@app.post("/evaluate", response_model=DecisionResponse)
def evaluate(req: PurchaseRequest):
    result = decide(req)
    if result.decision == Decision.APPROVE:
        charge(req.user_id, req.price, req.request_id)
    return result