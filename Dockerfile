FROM python:3.9-slim-buster

COPY ./requirements.txt .
COPY ./amongus_images ./amongus_images 
COPY ./main.py ./main.py 
COPY ./api ./api
COPY ./api/inputs ./api/inputs

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]

