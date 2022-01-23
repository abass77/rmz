import requests
import base64

URL = "http://localhost:500/add_face"

#  first, encode our image with base64
with open("block.png", "rb") as imageFile:
    img = base64.b64encode(imageFile.read())

response = requests.post(URL, data={"name":"obama", "img":str(img)})
print(response.content)