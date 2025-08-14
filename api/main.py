from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

APP_NAME = "omni-app"

request_counter = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["app_name", "method", "endpoint", "http_status"],
)
request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["app_name", "endpoint"],
)

app = FastAPI()

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    request_counter.labels(APP_NAME, request.method, request.url.path, response.status_code).inc()
    request_latency.labels(APP_NAME, request.url.path).observe(duration)
    return response

@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
async def read_root():
    return {"status": "ok"}

