from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# This class defines exactly what fields the incoming JSON must have.
# FastAPI uses this to automatically validate the request for you.
class ProrationRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: float
    days_in_actual_month: float
    spec: str  # will be "v1" or "v2"


@app.post("/proration")
def calculate_proration(req: ProrationRequest):
    price_difference = req.new_price - req.old_price

    if req.spec == "v1":
        # Legacy rule: always divide by exactly 30 days
        charge = price_difference * (req.days_remaining / 30)
    elif req.spec == "v2":
        # Corrected rule: divide by the real number of days in the month
        charge = price_difference * (req.days_remaining / req.days_in_actual_month)
    else:
        # Fallback in case spec is something unexpected
        charge = 0.0

    return {"charge": round(charge, 2)}


# Optional: a simple homepage so you can confirm the server is alive
@app.get("/")
def root():
    return {"status": "running"}
