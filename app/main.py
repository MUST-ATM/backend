from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import upload,balance,account
from contextlib import asynccontextmanager
from .dataBase import init, close

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    await init()  # 初始化数据库
    yield
    # 应用关闭时执行
    await close()  # 关闭数据库连接

app = FastAPI(lifespan=lifespan)

app.include_router(upload.router)
app.include_router(balance.router)
app.include_router(account.router) 

@app.get("/")
def main():
    content = """
<body>
<form action="/upload/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/upload/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
