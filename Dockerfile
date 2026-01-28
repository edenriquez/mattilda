FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY schema.prisma .
RUN prisma generate

COPY . .

ENV FLASK_APP=src/app.py
ENV FLASK_DEBUG=1
ENV PYTHONPATH=.

CMD prisma migrate deploy && flask run --host=0.0.0.0 --port=5001
