FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir stomp.py

COPY test_request.py .

CMD ["python", "test_request.py"]