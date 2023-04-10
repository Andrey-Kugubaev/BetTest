FROM python:3.10-slim

WORKDIR /receiver

COPY requirements.txt .
COPY . /receiver

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "-m", "app"]
