FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080

CMD exec gunicorn --bind :$PORT \
    --workers 4 \
    --threads 8 \
    --timeout 300 \
    --keep-alive 5 \
    --worker-class=gthread \
    --limit-request-line 8190 \
    --limit-request-fields 1000 \
    --limit-request-field_size 8190 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    proxy:app 
