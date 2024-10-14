# filename: upload.py
# description: This file handles the image upload functionality, utilizing chunked streaming transmission.
# author: xiaohuo233 & Cieres
# date: 2024-09-21
# version: 1.0
"""
After initial testing, this file currently meets the requirements. 
It may be further modified when integrating with the database in the future.
"""

from fastapi import APIRouter, Request
import aiofiles
from app.face_module.FacePerception.FaceRecognition import faceRecognitionByPath

router = APIRouter()

@router.post("/upload/")
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
        return faceRecognitionByPath(filename)
    except Exception:
        return {"message": "There was an error uploading the file"}