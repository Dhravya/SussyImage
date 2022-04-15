import os
import requests

assert os.path.exists("output.png")

response = requests.post("http://localhost:8000/", files={"input_image": open("output.png", "rb")})

# Save response to api_response.png
with open("api_response.png", "wb") as f:
    f.write(response.content)