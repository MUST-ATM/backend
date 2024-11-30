# balance.py
from fastapi import APIRouter, Request,HTTPException
from app.dataBase import get_connection
import aiosqlite

router = APIRouter()
DATABASE = "app/database.db"

# Balance Change API
@router.post("/account/balance/change", tags=["balance"])
async def change_balance(request: Request):
    data = await request.json()
    user_id = int(data.get("user_id"))
    amount = float(data.get("amount"))
    currency = data.get("currency")


    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        if currency == "CNY":
            async with db.execute("SELECT * FROM user") as cursor:
                print("Reading...")
                async for row in cursor:
                    if int(row['user_id']) == user_id:
                        print("Writting...")
                        await db.execute("UPDATE balance SET foreign_account = ? WHERE user_id = ? ", (amount, user_id))
                        await db.commit()
                        assert db.total_changes > 0

                        return HTTPException(status_code=200, detail="Success")
                
        elif currency == "MOP":
             async with db.execute("SELECT * FROM user") as cursor:
                print("Reading...")
                async for row in cursor:
                    if int(row['user_id']) == user_id:
                        print("Writting...")
                        await db.execute("UPDATE balance SET mop_account = ? WHERE user_id = ? ", (amount, user_id))
                        await db.commit()
                        assert db.total_changes > 0

                        return HTTPException(status_code=200, detail="Success")
                    
        elif currency == "HKD":
            async with db.execute("SELECT * FROM user") as cursor:
                print("Reading...")
                async for row in cursor:
                    if int(row['user_id']) == user_id:
                        print("Writting...")
                        await db.execute("UPDATE balance SET hkd_account = ? WHERE user_id = ? ", (amount, user_id))
                        await db.commit()
                        assert db.total_changes > 0

                        return HTTPException(status_code=200, detail="Success")

    return HTTPException(status_code=200, detail="Success")