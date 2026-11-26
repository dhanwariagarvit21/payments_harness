# Agentic Payments Harness

A guardrail layer between an AI shopping agent and a payment system. The agent
proposes a purchase under a user-given **mandate** (allowed categories, price
limit, total budget, expiry). The harness decides whether to **approve**, ask
for **re-authentication**, or **block**, and explains why.

```
mock agent  ->  harness (FastAPI)  ->  mock bank
                  |
              rules engine  <-  SQLite (purchase history, spend ledger, attempts)
```

## How decisions work

Each check returns a signal with a weight. The engine sums triggered weights:
1.0 or more means re-authentication. Block only happens after repeated failed
attempts under one mandate. See `docs/scenarios.md` for every scenario.

Checks: price limit, category, expiry, total budget, new item or category,
quantity spike and drop, purchase frequency for non-perishables.

## Run it (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m scripts.seed_history
python -m uvicorn harness.main:app --reload
```

In a second terminal (venv active):

```powershell
python -m scripts.demo
```

## Tests

```powershell
python -m pytest -v
```

Tests use a fresh temporary database each time and do not need the server.

## Roadmap

- Pooled purchase-pattern database (is this item unlikely across all users?)
- LLM check that the item matches the user's original request
- Failure handling: re-auth flow, bank declines, timeouts, retries