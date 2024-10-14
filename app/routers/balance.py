# balance.py
from fastapi import APIRouter, Request,HTTPException
from app.dataBase import get_connection

router = APIRouter()

# Deposit API
@router.post("/balance/deposit", tags=["balance"])
async def deposit(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    db = await get_connection()
    async with db.execute("SELECT hkd_account FROM balance WHERE user_id = ?", (user_id,)) as cursor:
        balance = await cursor.fetchone()
        if not balance:
            raise HTTPException(status_code=405, detail="Balance not found")

        new_balance = balance[0] + amount
        await db.execute("UPDATE balance SET hkd_account = ? WHERE user_id = ?", (new_balance, user_id))
    await db.commit()
    await db.close()

    return True

# Withdrawal API
@router.post("/balance/withdrawal", tags=["balance"])
async def withdrawal(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    db = await get_connection()

    async with db.execute("SELECT hkd_account FROM balance WHERE user_id = ?", (user_id,)) as cursor:
        balance = await cursor.fetchone()

        if not balance:
            raise HTTPException(status_code=405, detail="Balance not found")

        if balance[0] < amount:
            raise HTTPException(status_code=407, detail="Insufficient balance")

        new_balance = balance[0] - amount
        await db.execute("UPDATE balance SET hkd_account = ? WHERE user_id = ?", (new_balance, user_id))

    await db.commit()
    
    return True
