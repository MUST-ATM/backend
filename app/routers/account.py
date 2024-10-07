from fastapi import APIRouter,HTTPException
from app.models import User,Balance

router = APIRouter()

# 写死数据 测试用
class MockDatabase:
    def __init__(self):
        self.users = {
            "user1": {"name": "Alice", "userID": "00001"},
            "user2": {"name": "Bob", "userID": "00002"},
        }
        # 人脸识别码
        self.faces = {
            "known-face-id-1": "user1",
            "known-face-id-2": "user2",
        }
        # 银行卡信息(三币)
        self.cards = {
            "user1": {
                "foreign_account": 5000.0,
                "hkd_account": 3000.0,
                "mop_account": 2000.0
            },
            "user2": {
                "foreign_account": 1000.0,
                "hkd_account": 1500.0,
                "mop_account": 700.0
            }
        }

    def get_user_info(self, user_id: str):
        return self.users.get(user_id)

    def get_user_id_by_face(self, face_id: str):
        return self.faces.get(face_id)
    
    def get_card_info(self, user_id: str, currency: str):
        return self.cards[user_id].get(f"{currency}_account")

@router.get("/account/user/{user_id}", tags=["account"])
async def get_user_info(user_id: str):
    user = await User.filter(user_id=user_id).first()
    return {"userID": user.user_id, "name": user.name}

@router.get("/account/face/{face_id}", tags=["account"])
async def get_user_id_by_face(face_id: str):
    user = await User.filter(face_id=face_id).first()
    return {"userID": user.user_id}

@router.get("/account/card/{user_id}/{currency}", tags=["account"])
async def get_balance_by_currency(user_id: str, currency: str):
    user = await User.filter(user_id=user_id).first()
    balance = await Balance.filter(user=user).first()

    # 获取特定货币的余额
    if currency == "foreign":
        balance_value = balance.foreign_account
    elif currency == "hkd":
        balance_value = balance.hkd_account
    elif currency == "mop":
        balance_value = balance.mop_account
    else:
        raise HTTPException(status_code=400, detail="Invalid currency type")

    return {"balance": balance_value}
