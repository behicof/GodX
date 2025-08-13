from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, REGISTRY

app = FastAPI(title="OMNI Metrics API")

# Simple counter
requests_total = Counter("requests_total", "Total requests served")

@app.get("/")
def index():
    requests_total.inc()
    return {"msg": "hello"}

@app.get("/metrics")
def metrics():
    # Default Prometheus exposition format
    return Response(
        generate_latest(REGISTRY),
        media_type="text/plain; version=0.0.4",
    )
