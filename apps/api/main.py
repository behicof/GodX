from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, REGISTRY

app = FastAPI(title="OMNI Metrics API")

hits = Counter("api_requests_total", "Total API requests")

@app.get("/")
def root():
    hits.inc()
    return {"ok": True}

@app.get("/metrics")
def m():
    return Response(generate_latest(REGISTRY), media_type="text/plain; version=0.0.4")
