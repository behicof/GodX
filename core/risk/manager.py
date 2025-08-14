import time
from libs.metrics import counter, gauge


class RiskManager:
    """Very small placeholder risk manager."""

    check_latency = gauge(
        "risk_manager_check_latency_seconds", "Latency of risk checks"
    )
    check_errors = counter(
        "risk_manager_check_errors_total", "Total errors during risk checks"
    )

    def check(self, opportunity: dict) -> bool:
        """Approve trade if quantity is positive."""
        start = time.perf_counter()
        try:
            return opportunity.get("qty", 0) > 0
        except Exception:
            self.check_errors.inc()
            raise
        finally:
            self.check_latency.set(time.perf_counter() - start)
