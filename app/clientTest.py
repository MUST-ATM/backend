<<<<<<< HEAD
=======
"""
This is a test file, used solely for testing the transmission functionality of upload.py.
Run this file after starting the Uvicorn server.
Note: The file path is hardcoded. If running on a different machine, 
you will need to modify it to the full path of the image to be tested on that machine.
"""
>>>>>>> db34c08f1ee02c2e889f2d8724a5baebda9abc99

import requests
import time

<<<<<<< HEAD
with open("C:\misc\image2.png", "rb") as f:
=======
with open("H:\Temp\pic\image.png", "rb") as f:
>>>>>>> db34c08f1ee02c2e889f2d8724a5baebda9abc99
    data = f.read()
   
url = 'http://127.0.0.1:8000/upload'
headers = {'filename': 'output.png'}

start = time.time()
r = requests.post(url=url, data=data, headers=headers)
end = time.time() - start

print(f'Elapsed time is {end} seconds.', '\n')
print(r.json())