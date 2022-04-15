from random import randint
from main import SussyImage
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI(title="Sussy Image API", description="A fastapi api for making amongus images")

@app.post("/")
def convert_to_sussy(input_image: UploadFile = File(...), atol: int = 30):
    r = randint(0, 5)
    path = f"./api/inputs/input_image{r}.png"
    with open(path, "wb") as f:
        f.write(input_image.file.read())

    sussy = SussyImage(input_img_path=path, emoji_size=50, width=2000)

    sussy.run(atol, show=False, save=True, save_path=path)
    return FileResponse(path, media_type="image/png")