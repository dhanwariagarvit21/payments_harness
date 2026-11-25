from harness.schemas import Decision, DecisionResponse, PurchaseRequest


def decide(req: PurchaseRequest) -> DecisionResponse:
    """Skeleton: approves everything. Real rules replace this later."""
    return DecisionResponse(
        request_id=req.request_id,
        decision=Decision.APPROVE,
        reason="skeleton: approve everything",
        signals=[],
    )	