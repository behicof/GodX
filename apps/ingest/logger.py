import asyncio
import json
import os
import time

import websockets
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

PUSHGW_URL = os.getenv('PUSHGW_URL', 'http://localhost:9091')
registry = CollectorRegistry()
price_gauge = Gauge('omni_mark_price', 'Mark price', ['symbol'], registry=registry)
lag_gauge = Gauge('omni_ws_lag_seconds', 'Websocket message lag', ['symbol'], registry=registry)

async def stream_mark_prices():
    url = 'wss://fstream.binance.com/ws/!markPrice@arr'
    while True:
        try:
            async with websockets.connect(url) as ws:
                async for msg in ws:
                    data = json.loads(msg)
                    now = time.time()
                    for item in data:
                        symbol = item['s']
                        price = float(item['p'])
                        event_ts = item['E'] / 1000
                        lag = max(0.0, now - event_ts)
                        price_gauge.labels(symbol=symbol).set(price)
                        lag_gauge.labels(symbol=symbol).set(lag)
                    push_to_gateway(PUSHGW_URL, job='omni_logger', registry=registry)
        except Exception:
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(stream_mark_prices())
