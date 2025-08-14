import time
from libs.metrics import make_logger_metrics, push_metrics

r, quotes_c, lag_g, err_c = make_logger_metrics()

def measure_lag_ms(last_ts_ms: int) -> float:
    return max(0, time.time()*1000 - last_ts_ms)

def run_once():
    try:
        # ... دریافت کوئوت‌ها (ts_ms را از منبع واقعی بگیر)
        ts_ms = int(time.time()*1000)  # نمونه
        quotes_c.inc()
        lag_g.set(measure_lag_ms(ts_ms))
    except Exception:
        err_c.inc()
    finally:
        push_metrics(r, grouping_key={"script":"logger"})

if __name__ == "__main__":
    while True:
        run_once()
        time.sleep(5)
