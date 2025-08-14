import time
from libs.metrics import mk_logger, push_metrics

r, quotes_c, lag_g, err_c = mk_logger()


if __name__ == "__main__":
    while True:
        try:
            quotes_c.inc()
            lag_g.set(100)
            push_metrics(r, grouping_key={"script": "logger"})
        except Exception:
            err_c.inc()
            push_metrics(r, grouping_key={"script": "logger", "err": "1"})
        time.sleep(5)

