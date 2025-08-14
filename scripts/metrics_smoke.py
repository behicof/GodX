#!/usr/bin/env python3
"""Minimal Prometheus metrics exporter for smoke testing.

Usage:
    python scripts/metrics_smoke.py --port 8000

This script starts a Prometheus exporter on the given port and updates a
single gauge with random values a few times before exiting.
"""

import argparse
import random
import time

from prometheus_client import Gauge, start_http_server


def main(port: int) -> None:
    gauge = Gauge("godx_smoke_metric", "Random value for smoke testing")
    start_http_server(port)
    for _ in range(5):
        gauge.set(random.random())
        time.sleep(0.5)
    print(f"Exported dummy metrics on http://localhost:{port}/metrics")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a tiny metrics exporter")
    parser.add_argument("--port", type=int, default=8000, help="Port to export metrics on")
    args = parser.parse_args()
    main(args.port)
