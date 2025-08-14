from fastapi import FastAPI, Response
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest, multiprocess, REGISTRY

app = FastAPI()

@app.get("/metrics")
def metrics():
    # اگر multi-process نیستید، مستقیماً generate_latest(REGISTRY)
    data = generate_latest(REGISTRY)
    return Response(data, media_type=CONTENT_TYPE_LATEST)
