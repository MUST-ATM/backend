import aiosqlite
from fastapi import APIRouter,HTTPException
from app.dataBase import DATABASE

router = APIRouter()

@router.get("/account/user/{user_id}", tags=["account"])
async def get_user_info(user_id: str):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT user_id, name FROM user WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if not user:
                return {"message": "User not found"}
            return {"userID": user[0], "name": user[1]}

@router.get("/account/face/{face_id}", tags=["account"])
async def get_user_id_by_face(face_id: str):
    return {"userID": "user_id_placeholder"}

@router.get("/account/card/{user_id}/{currency}", tags=["account"])
async def get_balance_by_currency(user_id: str, currency: str):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT foreign_account, hkd_account, mop_account FROM balance WHERE user_id = ?", (user_id,)) as cursor:
            balance = await cursor.fetchone()
            if not balance:
                return {"message": "Balance not found"}

            if currency == "foreign":
                balance_value = balance[0]
            elif currency == "hkd":
                balance_value = balance[1]
            elif currency == "mop":
                balance_value = balance[2]
            else:
                return {"message": "Invalid currency type"}

    return {"balance": balance_value}
