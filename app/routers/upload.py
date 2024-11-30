# filename: upload.py
# description: This file handles the image upload functionality, utilizing chunked streaming transmission.
# author: xiaohuo233 & Cieres
# date: 2024-09-21
# version: 1.0
"""
After initial testing, this file currently meets the requirements.
It may be further modified when integrating with the database in the future.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import aiosqlite
from app.face_module.FacePerception.FaceRecognition import faceRecognitionByPath
from app.dataBase import get_connection
import asyncio

DATABASE = "app/database.db"

router = APIRouter()

@router.post("/upload/face-reco", tags=["upload"])
async def upload(request: Request):
    """
    Handles file upload via chunked streaming transmission.
    The uploaded file is written to disk asynchronously, then passed to the face recognition function.


    Args:
        request (Request): The incoming request containing the file data.

    Returns:
        A dictionary containing either the face recognition result (name) or an error message.
    """
    # Extract the filename from the request headers.(none extra protect)
    async with aiofiles.open("app/received/capture.jpg", 'wb') as f:
        async for chunk in request.stream():
            await f.write(chunk)
    # After the file is written, call the face recognition function on the saved file.
    try:
        print("faceRecoing")
        username =  faceRecognitionByPath('app/received/capture.jpg')
    except:
        return JSONResponse(status_code=410, content={"detail": "Error FaceRecognition"})
    
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM user") as cursor:
            async for row in cursor:
                print(row['name'])
                if row['name'] == username:
                    return {"username": row['user_id']}
                else:
                    return JSONResponse(status_code=404, content={"detail": "User not found"})


@router.post("/upload/face-anti", tags=["upload"])
async def upload(request: Request):
    from app.face_module.FaceAntiSpoofing.FaceAntiSpoofing import faceAntiSpoofingByPath
    # Extract the filename from the request headers.(none extra protect)
    async def run_sync(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, *args, **kwargs)

    # 使用异步包装器调用faceAntiSpoofingByPath函数
    result = await run_sync(faceAntiSpoofingByPath, "app/received/capture.jpg")
    if result:
       return HTTPException(status_code=200, detail="Success")
    else:
        return JSONResponse(status_code=411, content={"detail": "ErrorFaceAntiSpoofing"})
"""    if  faceAntiSpoofingByPath("capture2.jpg"):
        raise HTTPException(status_code=200, detail="Success")
    else:
        raise HTTPException(status_code=411, detail="Error FaceAntiSpoofing")
        return JSONResponse(status_code=500, content={"detail": str(e)})
        """