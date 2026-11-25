from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PurchaseRequest(BaseModel):
    user_id: str
    item: str
    price: float


@app.post("/evaluate")
def evaluate(req: PurchaseRequest):
    return {"decision": "approve", "reason": f"{req.item} looks fine"}