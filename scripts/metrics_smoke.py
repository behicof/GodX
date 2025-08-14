#!/usr/bin/env python3
"""Simple metrics smoke test.

Starts a dummy metrics backend in *export* mode, emits a couple of sample
values and performs a push that is a no-op.  The script is meant to mimic
how a metrics pipeline would be exercised end-to-end during a quick health
check.
"""

from __future__ import annotations


class Metrics:
    """Minimal stand-in metrics backend."""

    def __init__(self, mode: str = "export") -> None:
        self.mode = mode
        self.samples: list[tuple[str, float]] = []

    def emit(self, name: str, value: float) -> None:
        """Record a metric sample."""
        self.samples.append((name, value))
        print(f"emit {name}={value}")

    def push(self) -> None:
        """Push samples upstream (no-op)."""
        print(f"push ({self.mode}) with {len(self.samples)} samples: noop")


def main() -> None:
    metrics = Metrics(mode="export")
    metrics.emit("orders_total", 2)
    metrics.emit("latency_ms", 5)
    metrics.push()


if __name__ == "__main__":  # pragma: no cover - smoke script
    main()
