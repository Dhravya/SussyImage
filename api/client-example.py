import os
import requests

assert os.path.exists("assets/lonamisa.png")

response = requests.post("https://sussy.api.dhravya.dev", files={"input_image": open("assets/lonamisa.png", "rb")})

print(response)

# Save response to api_response.png
with open("api_response.png", "wb") as f:
    f.write(response.content)