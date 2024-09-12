from fastapi import File, UploadFile
from fastapi import APIRouter
from app.face_module.FacePerception.FaceRecognition import faceRecognition
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/upload/",tags=["upload"])
async def create_upload_files(files: list[UploadFile]=None):
    for file in files:
        name = faceRecognition(await file.read()) 
        if name!=None:
            #anti-spoofing program
            #...
            #if anti-spoofing program is true:
            return {"name":name}
            #else:
            #return JSONResponse(status_code=400, content={"message": "Face is spoofed"})
    return JSONResponse(status_code=404, content={"message": "Face not detected"})