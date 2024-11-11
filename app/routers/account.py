import aiosqlite

from fastapi import APIRouter, HTTPException
from app.dataBase import DATABASE
from app.face_module.FacePerception.FaceRecognition import newFace
router = APIRouter()

@router.get("/account/face/{face_id}", tags=["account"])
async def get_user_info(face_id: str):
    """
    Get the user information for the specified face ID.
    Args:
        face_id (str): The face ID of the account to retrieve.
    Returns:
        A dictionary containing the user ID of the account holder.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT user_id FROM face WHERE name = ?", (face_id,)) as cursor:
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"userID": user[0]}

@router.get("/account/card/{user_id}/{currency}", tags=["account"])
async def get_balance_by_currency(user_id: str, currency: str):
    """
    Get the balance of the specified currency for the specified user ID.
    Args:
        user_id (str): The user ID of the account to retrieve.
        currency (str): The currency type to retrieve (foreign, hkd, mop).
    Returns:
        A dictionary containing the balance of the specified currency.
    """
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT foreign_account, hkd_account, mop_account FROM balance WHERE user_id = ?", (user_id,)) as cursor:
            balance = await cursor.fetchone()
            if not balance:
                raise HTTPException(status_code=405, detail="Balance not found")

            if currency == "foreign":
                balance_value = balance[0]
            elif currency == "hkd":
                balance_value = balance[1]
            elif currency == "mop":
                balance_value = balance[2]
            else:
                raise HTTPException(status_code=406, detail="Invalid currency type")

    return {"balance": balance_value}

@router.post("/account/create", tags=["account"])
async def create_user(user_id: str, name: str,imagePath:str):
    """
    Create a new user account with the specified user ID and name.
    Args:
        user_id (str): The user ID of the new account.
        name (str): The name of the new account holder.
    Returns:
        True if the account was created successfully.
    """
    try:
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute("INSERT INTO user (user_id, name) VALUES (?, ?)", (user_id, name))
            await db.execute("INSERT INTO balance (user_id, foreign_account, hkd_account, mop_account) VALUES (?, ?, ?, ?)", (user_id, 0.0, 0.0, 0.0))
            await db.commit()
        newFace(imagePath,user_id)
        return True
    except:
        raise HTTPException(status_code=409, detail="Error Account Creation")

@router.post("/account/delete", tags=["account"])
async def delete_user(user_id: str):
    """
    Delete the user account with the specified user ID.
    Args:
        user_id (str): The user ID of the account to be deleted.
    Returns:
        True if the account was deleted successfully.
    """
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM balance WHERE user_id = ?", (user_id,))
        await db.commit()
    return True