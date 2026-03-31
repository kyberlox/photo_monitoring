FROM python:3.13-slim

WORKDIR /data/app

COPY ./requirements.txt /data/app/requirements.txt

RUN apt-get update && pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--port", "8000"]