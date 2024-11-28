# backend
The backend part of MUST ATM system based on Python.

## What's MUST ATM
This is a final project of the course "Software Engineering" in the Faculty of Innovation Engineering, Macau University of Science and Technology. The project is a smart ATM system that can recognize the user's face and provide a personalized service. The backend of system is based on the FastAPI framework and the face_recognition library.
## Installation
Please install the fastapi and uvicorn first
```bash
mamba create -n api python=3.10
mamba activate api 
pip install fastapi
pip install uvicorn
```
Other requirements
````bash
pip install aiofiles
pip install aiosqlite
````

## Environment
Ensure the python running path is the parent floder of app
If you are using windows
```bash
set PYTHONPATH=.
```
Linux or MacOS
```bash
export PYTHONPATH=.
```
## RUN
Run the server
```bash
python -m uvicorn app.main:app --reload
```

## Face Recognition Module
The face recognition module is based on the face_recognition library.
You have to install the face_recognition library first.
```bash
pip install face_recognition
```
Then you need clone our face recognition module in app folder
```bash
cd app
git clone https://github.com/MUST-ATM/face_module.git
```

## Database
TBD

## API
TBD

## RouteMap
TBD

## Contributors
TBD