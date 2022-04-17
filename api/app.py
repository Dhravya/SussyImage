from random import randint
from main import SussyImage
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI(title="Sussy Image API", description="A fastapi api for making amongus images")

@app.post("/amongus")
def convert_to_sussy(input_image: UploadFile = File(...), atol: int = 30, width: int = 1500, compare: bool = False):
    r = randint(0, 5)
    path = f"./api/inputs/input_image{r}.png"
    with open(path, "wb") as f:
        f.write(input_image.file.read())

    if width > 3000:
        width = 3000

    sussy = SussyImage(input_img_path=path, emoji_size=30, width=width)

    sussy.run(atol, show=False, save=True, save_path=path, compare=compare)
    return FileResponse(path, media_type="image/png")