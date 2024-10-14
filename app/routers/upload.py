# filename: upload.py
# description: This file handles the image upload functionality, utilizing chunked streaming transmission.
# author: xiaohuo233 & Cieres
# date: 2024-09-21
# version: 1.0
"""
After initial testing, this file currently meets the requirements.
It may be further modified when integrating with the database in the future.
"""

from fastapi import APIRouter, Request,HTTPException
import aiofiles

from app.face_module.FacePerception.FaceRecognition import faceRecognitionByPath
from app.face_module.FaceAntiSpoofing import faceAntiSpoofingByPath
from app.dataBase import get_connection

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
    try:
        # Extract the filename from the request headers.(none extra protect)
        filename = request.headers['filename']
        async with aiofiles.open(filename, 'wb') as f:
            async for chunk in request.stream():
                await f.write(chunk)

        # After the file is written, call the face recognition function on the saved file.
        try:
            user_id =  faceRecognitionByPath(filename)
        except:
            raise HTTPException(status_code=410, detail="Error FaceRecognition")
        try:
            db = await get_connection()
        except:
            raise HTTPException(status_code=412, detail="Database connection error")
        async with db.execute("SELECT name FROM user WHERE user_id = ?", (user_id)) as cursor:
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"username" : user[0]}
    except Exception:
        raise HTTPException(status_code=408, detail="Error uploading")

@router.post("/upload/face-anti", tags=["upload"])
async def upload(request: Request):
    """
    Handles file upload via chunked streaming transmission.
    The uploaded file is written to disk asynchronously, then passed to the face recognition function.


    Args:
        request (Request): The incoming request containing the file data.

    Returns:
        A dictionary containing either the face recognition result (name) or an error message.
    """
    try:
        # Extract the filename from the request headers.(none extra protect)
        filename = request.headers['filename']
        async with aiofiles.open(filename, 'wb') as f:
            async for chunk in request.stream():
                await f.write(chunk)

        # After the file is written, call the face recognition function on the saved file.
        try:
            return faceAntiSpoofingByPath(filename)
        except:
            raise HTTPException(status_code=411, detail="Error FaceAntiSpoofing")
    except Exception:
        raise HTTPException(status_code=408, detail="Error uploading")