from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ExecResult:
    """Result of an execution attempt."""
    ok: bool
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
