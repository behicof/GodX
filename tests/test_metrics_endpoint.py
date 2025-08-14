from fastapi.testclient import TestClient

from api.main import app


def test_metrics_endpoint_exposes_prometheus_metrics():
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_info" in response.text
