import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import asyncio
from app.dataBase import create_tables, insert_initial_data, get_connection

async def setup_database():
    """初始化数据库"""
    await create_tables()
    await insert_initial_data()

async def teardown_database():
    """清理数据库"""
    db = await get_connection()
    try:
        await db.execute("DELETE FROM user")
        await db.execute("DELETE FROM balance")
        await db.commit()
    finally:
        await db.close()


asyncio.run(setup_database())

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_get_user_info():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/account/user/00001")
        assert response.status_code == 200
        assert response.json() == {"userID": "00001", "name": "Alice"}

@pytest.mark.asyncio
async def test_get_balance_by_currency():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/account/card/00001/mop")
        assert response.status_code == 200
        assert response.json() == {"balance": 2000.0}

@pytest.mark.asyncio
async def test_deposit():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/balance/deposit", json={"user_id": "00001", "amount": 500})
        assert response.status_code == 200
        assert response.json() is True

@pytest.mark.asyncio
async def test_withdrawal():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/balance/withdrawal", json={"user_id": "00001", "amount": 1000})
        assert response.status_code == 200
        assert response.json() is True

@pytest.mark.asyncio
async def test_withdrawal_insufficient_balance():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/balance/withdrawal", json={"user_id": "00001", "amount": 5000})
        assert response.status_code == 200
        assert response.json() == {"message": "Insufficient balance"}

@pytest.fixture(scope="session", autouse=True)
def cleanup_database():
    yield  
    asyncio.run(teardown_database())
