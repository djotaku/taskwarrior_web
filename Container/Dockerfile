FROM docker.io/python:3.13-slim

RUN apt update && apt install -y taskwarrior gcc git

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install -e .
RUN pip install gunicorn

VOLUME /root/.task
EXPOSE 8000

WORKDIR /app/taskwarrior_web
CMD ["python", "app.py"]
