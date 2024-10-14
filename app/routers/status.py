from fastapi import APIRouter, Request,HTTPException

router = APIRouter()

status = {
    404: "User not found",
    405: "Balance not found",
    406: "Invalid currency type",
    407: "Insufficient balance",
    408: "Error uploading",
    409: "Error Account Creation"
}

@router.get("/status", tags=["status"])
async def getStatus():
    
    return status



"""
raise HTTPException(status_code=404, detail="User not found")
raise HTTPException(status_code=405, detail="Balance not found")
raise HTTPException(status_code=406, detail="Invalid currency type")
raise HTTPException(status_code=407, detail="Insufficient balance")
raise HTTPException(status_code=408, detail="Error uploading")
raise HTTPException(status_code=409, detail="Error Account Creation")
raise HTTPException(status_code=410, detail="Error FaceRecognition")
raise HTTPException(status_code=411, detail="Error FaceAntiSpoofing")
raise HTTPException(status_code=412, detail="Database connection error")
"""