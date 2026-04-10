FROM python:3.12-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

COPY app ./app
COPY nginx/backend.conf /etc/nginx/conf.d/default.conf

ENV PYTHONPATH=/app
EXPOSE 80

CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'" ]
