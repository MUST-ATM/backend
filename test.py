import os
import sys

from app.face_module.FaceAntiSpoofing.FaceAntiSpoofing import faceAntiSpoofingByPath
print(faceAntiSpoofingByPath("images/download.jpg"))

"""
import os

image_path = r"C:\misc\API\images\download.jpg"
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
else:
    print(f"File exists: {image_path}")



"""
