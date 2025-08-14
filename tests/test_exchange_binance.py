import os
import pytest

from requests import HTTPError
from core.exchange.binance import BinanceExchange


def test_get_mark_price():
    ex = BinanceExchange()
    try:
        price = ex.get_mark_price('BTCUSDT')
    except HTTPError as e:
        pytest.skip(f"HTTP error: {e}")
    assert price > 0


def test_get_funding_info():
    ex = BinanceExchange()
    try:
        info = ex.get_funding_info('BTCUSDT')
    except HTTPError as e:
        pytest.skip(f"HTTP error: {e}")
    assert 'lastFundingRate' in info


@pytest.mark.skipif(not os.getenv('BINANCE_API_KEY'), reason='no credentials')
def test_place_order_ioc_skip_without_keys():
    ex = BinanceExchange()
    with pytest.raises(Exception):
        ex.place_order_ioc('BTCUSDT', 'BUY', quantity=0.001, price=50000)
