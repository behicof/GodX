FROM python:3.11-slim
WORKDIR /app
COPY main.py .
RUN pip install fastapi uvicorn prometheus-client
CMD ["python","main.py"]
