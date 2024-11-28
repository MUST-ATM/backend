目前项目因路径问题，大多数路径都是本机绝对路径，测试路径写死，如下：

#1 FaceAntiSpoofing--FaceAntiSpoofing.py 中参数、模型文件位置    

line 125
def faceAntiSpoofingByPath(path):
    parser = argparse.ArgumentParser()
    parser.add_argument("--img", type=str, default=Image.open(path).convert('RGB').rotate(180))
    parser.add_argument("--gpu_ids", type=str, default="0")
    parser.add_argument("--root", type=str, default="")
    parser.add_argument("--preprocess", type=str, default="resize_crop_rotate_flip")
    parser.add_argument("--trainer", type=str, default="CLIP")
    parser.add_argument("--version", type=str, default="VL")
    parser.add_argument("--prompt", type=str, default="class")
    parser.add_argument("--model_dir", type=str, default="/data/mahui/UniAttackData/output//CLIP@class/vit_b16/p2.2@Physical@Physical@Digital/seed1/")
    parser.add_argument("--USE_CUDA", type=bool, default=True)
    parser.add_argument("--dataset_config_file", type=str, default="C:/misc/API/backend/app/face_module/FaceAntiSpoofing/configs/datasets/UniAttackData.yaml")
    parser.add_argument("--config_file", type=str, default="C:/misc/API/backend/app/face_module/FaceAntiSpoofing/configs/trainers/CLIP/rn50.yaml")
    parser.add_argument("--seed", type=int, default=1, help="only positive value enables a fixed seed")
    parser.add_argument("--backbone", type=str, default="", help="name of CNN backbone")
    parser.add_argument("--head", type=str, default="", help="name of head")
    parser.add_argument("--protocol", type=str, default="p1@UniAttack@UniAttack@UniAttack", help="protocol")
    parser.add_argument("--load-epoch", type=int, help="load model weights at this epoch for evaluation")
    parser.add_argument("--inference",default=True,action="store_true", help="inference mode")
    args,unknown = parser.parse_known_args()
    return main(args)
    #return True


#2 FacePerception--FaceRecognition.py 中，文件夹位置，以及创建newFace的位置

line 8
import face_recognition as FR
import cv2
import os
import pickle

FolderName = "C:\misc\API\images"
Database = r"C:\misc\API\backend\app\face_module\FacePerception\FaceDatabase"


line 117
## main function
if __name__ == '__main__':
	newFace(cv2.imread('C:/misc/API/backend/capture2.jpg'), 'shuheDONG')
	#print(faceRecognitionByPath(img_path='D:/PythonCode/Face-module/FacePerception/HaomingZou.jpg'))




#3 Routers--upload.py 中，图片上传位置与图片名称

line 23
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
    async with aiofiles.open("capture.jpg", 'wb') as f:
        async for chunk in request.stream():
            await f.write(chunk)
    # After the file is written, call the face recognition function on the saved file.
    try:
        print("faceRecoing")
        username =  faceRecognitionByPath('capture2.jpg')

#4 tFacePerception--test_FaceRecognition.py 中，测试文件的路径

line 21
if __name__ == "__main__":
    test_face_recognition_by_path()
    test_face_recognition_by_byte()