from orchestrator.metrics_hook import time_leg, mark_fill
import time, random

def mock_leg():
    time.sleep(random.uniform(0.05, 0.2))

time_leg(mock_leg)
mark_fill("BTCUSDT", 1.0)
