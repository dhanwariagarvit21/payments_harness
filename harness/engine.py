from harness import db
from harness.checks import (
    check_budget, check_category, check_expiry, check_frequency, check_new_item,
    check_price_limit, check_quantity_drop, check_quantity_spike,
)
from harness.schemas import Decision, DecisionResponse, PurchaseRequest, Signal

REAUTH_THRESHOLD = 1.0
MAX_FAILED_ATTEMPTS = 3

CHECKS = [
    check_price_limit, check_category, check_expiry, check_budget,
    check_new_item, check_quantity_spike, check_quantity_drop, check_frequency,
]


def decide(req: PurchaseRequest) -> DecisionResponse:
    mandate_id = getattr(req.mandate, "mandate_id", "default")
    failed = db.failed_attempts(mandate_id)
    if failed >= MAX_FAILED_ATTEMPTS:
        sig = Signal(name="too_many_attempts", triggered=True, weight=1.0,
                     detail=f"{failed} failed attempts under mandate {mandate_id}")
        return DecisionResponse(request_id=req.request_id, decision=Decision.BLOCK,
                                reason=sig.detail, signals=[sig])
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