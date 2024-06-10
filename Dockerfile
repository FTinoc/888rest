# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /888sports

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "--app", "sports", "init-db"]

CMD ["python3", "-m", "flask", "--app", "sports", "run", "--host=0.0.0.0"]

