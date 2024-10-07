
import requests
import time

with open("C:\misc\image2.png", "rb") as f:
    data = f.read()
   
url = 'http://127.0.0.1:8000/upload'
headers = {'filename': 'output.png'}

start = time.time()
r = requests.post(url=url, data=data, headers=headers)
end = time.time() - start

print(f'Elapsed time is {end} seconds.', '\n')
print(r.json())