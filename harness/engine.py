from harness.schemas import Decision, DecisionResponse, PurchaseRequest
from harness.checks import (
    check_category, check_expiry, check_frequency, check_new_item,
    check_price_limit, check_quantity_drop, check_quantity_spike,
)
REAUTH_THRESHOLD = 1.0
CHECKS = [
    check_price_limit, check_category, check_expiry,
    check_new_item, check_quantity_spike, check_quantity_drop, check_frequency,
]


def decide(req: PurchaseRequest) -> DecisionResponse:
    signals = [check(req) for check in CHECKS]
    triggered = [s for s in signals if s.triggered]
    score = sum(s.weight for s in triggered)

    if score >= REAUTH_THRESHOLD:
        decision = Decision.REAUTH
        reason = "; ".join(s.detail for s in triggered)
    else:
        decision = Decision.APPROVE
        reason = "no signals triggered"

    return DecisionResponse(
        request_id=req.request_id,
        decision=decision,
        reason=reason,
        signals=signals,
    )