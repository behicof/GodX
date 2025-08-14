import os
import time
import hmac
import hashlib
from typing import Any

import requests

from .base import Exchange

BASE_URL = "https://fapi.binance.com"


class BinanceExchange(Exchange):
    """Minimal Binance Futures exchange client."""

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict[str, Any]) -> dict[str, Any]:
        if not self.api_secret:
            raise RuntimeError("API secret required for private endpoints")
        query = "&".join(f"{k}={v}" for k, v in params.items())
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def get_mark_price(self, symbol: str) -> float:
        resp = self.session.get(f"{BASE_URL}/fapi/v1/premiumIndex", params={"symbol": symbol})
        resp.raise_for_status()
        data = resp.json()
        return float(data["markPrice"])

    def get_funding_info(self, symbol: str) -> dict[str, Any]:
        resp = self.session.get(f"{BASE_URL}/fapi/v1/premiumIndex", params={"symbol": symbol})
        resp.raise_for_status()
        data = resp.json()
        return {
            "lastFundingRate": float(data["lastFundingRate"]),
            "nextFundingTime": int(data["nextFundingTime"]),
        }

    def place_order_ioc(self, symbol: str, side: str, quantity: float, price: float) -> dict[str, Any]:
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "IOC",
            "quantity": quantity,
            "price": price,
            "timestamp": int(time.time() * 1000),
        }
        signed = self._sign(params)
        resp = self.session.post(f"{BASE_URL}/fapi/v1/order", params=signed)
        resp.raise_for_status()
        return resp.json()

    # required abstract method
    def place_order(self, symbol: str, side: str, quantity: float, price: float | None = None) -> dict:
        return self.place_order_ioc(symbol, side, quantity, price or 0.0)
