class RiskManager:
    """Very small placeholder risk manager."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def check(self, opportunity: dict) -> bool:
        """Approve trade if quantity is positive."""
        return opportunity.get("qty", 0) > 0
