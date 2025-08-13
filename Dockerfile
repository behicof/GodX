FROM python:3.11-slim@sha256:8df0e8faf75b3c17ac33dc90d76787bbbcae142679e11da8c6f16afae5605ea7

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn prometheus_client

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
