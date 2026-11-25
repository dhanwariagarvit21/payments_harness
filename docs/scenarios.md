# Purchase Scenarios

## Ask for re-authentication

| Scenario | Example |
| --- | --- |
| Non-perishable purchased more often than history shows | A third vacuum cleaner is an anomaly; the same frequency for perishables may be normal. |
| Item too far from the mandate description | An agent attempts to buy a gaming console even though the mandate specifies "laptop for coding." |
| Quantity spike versus history | A user normally orders 4 body washes per month and now attempts to order 8. |
| Quantity drop versus history | A user now orders 1 instead of the usual quantity. This is a weaker signal than a spike. |
| Item never appeared in the user's past orders | There is no history against which to compare the item. |
| Erratic purchase pattern | The behavior does not fit the user's past history, even if no individual rule is triggered. |

## Block / cancel mandate

| Scenario | Example |
| --- | --- |
| Too many attempts within a single mandate order | Repeated retries may indicate an agent loop or attack, so the payment is blocked and the mandate is cancelled. |