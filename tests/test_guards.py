from core.risk import guards


def test_slippage_and_latency_and_depth():
    book = {"expected": 100, "price": 100.0, "depth": 6000}
    assert guards.check_slippage(book, 35)
    assert guards.check_latency(700, 800)
    assert guards.check_depth(book, 5000)
    assert guards.check_liquidation("BTCUSDT", 0.2)
    book_bad = {"expected": 100, "price": 101, "depth": 1000}
    assert not guards.check_slippage(book_bad, 35)
    assert not guards.check_depth(book_bad, 5000)
