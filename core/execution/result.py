from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ExecResult:
    """Execution result for IOC orders."""

    ok: bool
    reason: str
    details: Dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0
