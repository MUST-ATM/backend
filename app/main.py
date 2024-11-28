# filename: main.py
# description: This file handles the backend API for the ATM project, including  upload, user creation, and balance updates.
# author: Cieres
# date: 2024-09-21
# version: 0.1

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import upload,balance,account
from contextlib import asynccontextmanager
from app.dataBase import create_tables, insert_initial_data
from app.dataBase import get_connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()  # 初始化数据库
    await insert_initial_data()
    print("Init done")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(upload.router)
app.include_router(balance.router)
app.include_router(account.router) 

# Simplified main page to display 'Hello'
@app.get("/")
async def main():
    content = """
<body>
<h1>Hello</h1>
</body>
    """
    return HTMLResponse(content=content)