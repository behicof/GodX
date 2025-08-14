from fastapi import FastAPI, Response
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import uvicorn

app = FastAPI()

@app.get("/healthz")
def healthz(): return {"ok": True}

@app.get("/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return Response(data, media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
