# balance.py
from fastapi import APIRouter, Request
from app.models import User, Balance

router = APIRouter()

# Deposit API
@router.post("/balance/deposit", tags=["balance"])
async def deposit(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    user = await User.filter(user_id=user_id).first()
    balance = await Balance.filter(user=user).first()
    balance.hkd_account += amount
    await balance.save()

    return True

# Withdrawal API
@router.post("/balance/withdrawal", tags=["balance"])
async def withdrawal(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    user = await User.filter(user_id=user_id).first()
    balance = await Balance.filter(user=user).first()
    
    if balance.hkd_account < amount:
        return False

    balance.hkd_account -= amount
    await balance.save()

    return True