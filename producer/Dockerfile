FROM python:3.10-slim

WORKDIR /producer

COPY requirements.txt .
COPY . /producer

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "app"]
