from apps.backtester.metrics import run_backtest

class BT:
    def __iter__(self):
        import time
        for _ in range(5):
            time.sleep(0.1)
            yield None

    def pnl(self):
        return 42.0

run_backtest(BT())
