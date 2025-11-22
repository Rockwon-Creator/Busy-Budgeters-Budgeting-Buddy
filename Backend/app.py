from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from BudgetingBuddy import BudgetingBuddy 

app = FastAPI()

# Enable CORS (for local development / allowing requests from a Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Later restrict this when a final domain is set
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcRequest(BaseModel):
    mode: str                     # "final" | "time" | "deposit"
    balance: float                # Starting balance
    deposit: Optional[float] = 0  # Monthly deposit (meaning differs by mode)
    months: int                   # Savings period in months
    rate: float                   # Annual interest rate (decimal, e.g. 0.02 = 2%)
    goal: Optional[float] = None  # Goal amount (required for time/deposit modes)

class CalcResponse(BaseModel):
    series: List[float]
    total: float
    contrib: float
    interestEarned: float
    monthsNeeded: Optional[int] = None
    requiredDeposit: Optional[float] = None


def projection_final(balance: float, deposit: float, months: int, rate_decimal: float):
    """
    Calculates the final balance using BudgetingBuddy for the 'final' mode.
    Also generates a monthly balance series (deposit → interest order).
    """
    b = BudgetingBuddy()
    b.set_startingbalance(balance)
    b.set_monthlydeposit(deposit)
    b.set_savingperiod(months)
    b.set_monthsyears("Months")
    b.set_interestrate(rate_decimal * 100)  # Convert 0.02 → 2.0 (%)

    total = b.calculate_finalbalance()

    # Create monthly projection series (deposit first → apply interest)
    monthly_interest = (b.interest_rate / 100) / 12
    current = balance
    series = []
    for _ in range(months):
        current += deposit
        current *= (1 + monthly_interest)
        series.append(round(current, 2))

    contrib = balance + deposit * months
    interest = round(total - contrib, 2)

    return {
        "series": series,
        "total": round(total, 2),
        "contrib": round(contrib, 2),
        "interestEarned": interest,
    }


def time_to_goal(balance: float, deposit: float, rate_decimal: float, goal: float, max_months: int = 600):
    """
    Calculates how many months are required to reach a target goal.
    Uses deposit → interest monthly compounding.
    """
    if deposit <= 0:
        raise HTTPException(status_code=400, detail="Monthly deposit must be > 0 for time mode.")

    b = BudgetingBuddy()
    b.set_startingbalance(balance)
    b.set_monthlydeposit(deposit)
    b.set_finalbalance(goal)
    b.set_monthsyears("Months")
    b.set_interestrate(rate_decimal * 100)

    monthly_interest = (b.interest_rate / 100) / 12
    current = balance
    months = 0
    series = []

    while current < goal and months < max_months:
        current += deposit
        current *= (1 + monthly_interest)
        months += 1
        series.append(round(current, 2))

    if months == max_months and current < goal:
        raise HTTPException(status_code=400, detail="Goal not reachable within 600 months.")

    contrib = balance + deposit * months
    total = round(current, 2)
    interest = round(total - contrib, 2)

    return {
        "series": series,
        "total": total,
        "contrib": contrib,
        "interestEarned": interest,
        "monthsNeeded": months,
    }


def deposit_for_goal(balance: float, months: int, rate_decimal: float, goal: float):
    """
    Calculates the required monthly deposit needed to reach a goal within a fixed number of months.
    """
    if months <= 0:
        raise HTTPException(status_code=400, detail="Months must be > 0 for deposit mode.")

    b = BudgetingBuddy()
    b.set_startingbalance(balance)
    b.set_savingperiod(months)
    b.set_monthsyears("Months")
    b.set_finalbalance(goal)
    b.set_interestrate(rate_decimal * 100)

    monthly = b.calculate_monthlydeposit()

    # Build projection series using monthly deposit → interest compounding
    monthly_interest = (b.interest_rate / 100) / 12
    current = balance
    series = []
    for _ in range(months):
        current += monthly
        current *= (1 + monthly_interest)
        series.append(round(current, 2))

    contrib = balance + monthly * months
    total = round(current, 2)
    interest = round(total - contrib, 2)

    return {
        "series": series,
        "total": total,
        "contrib": contrib,
        "interestEarned": interest,
        "requiredDeposit": round(monthly, 2),
    }


@app.post("/api/calculate", response_model=CalcResponse)
def calculate(req: CalcRequest):
    """
    Main API endpoint for all calculation modes.
    Validates input and routes to the corresponding calculator function.
    """
    mode = req.mode

    if req.months < 1 or req.months > 600:
        raise HTTPException(status_code=400, detail="Months must be between 1 and 600.")

    if req.rate < 0 or req.rate > 0.10:
        raise HTTPException(status_code=400, detail="Rate must be between 0 and 0.10 (0%–10%).")

    if mode in ("time", "deposit") and (req.goal is None or req.goal <= 0):
        raise HTTPException(status_code=400, detail="Goal must be > 0 for this mode.")

    if mode == "final":
        result = projection_final(req.balance, req.deposit or 0, req.months, req.rate)
        return CalcResponse(**result)

    elif mode == "time":
        result = time_to_goal(req.balance, req.deposit or 0, req.rate, req.goal)
        return CalcResponse(
            series=result["series"],
            total=result["total"],
            contrib=result["contrib"],
            interestEarned=result["interestEarned"],
            monthsNeeded=result["monthsNeeded"],
        )

    elif mode == "deposit":
        result = deposit_for_goal(req.balance, req.months, req.rate, req.goal)
        return CalcResponse(
            series=result["series"],
            total=result["total"],
            contrib=result["contrib"],
            interestEarned=result["interestEarned"],
            requiredDeposit=result["requiredDeposit"],
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid mode.")
