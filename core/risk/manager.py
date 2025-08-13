class RiskManager:
    """Very small placeholder risk manager."""

    def check(self, opportunity: dict) -> bool:
        """Approve trade if quantity is positive."""
        return opportunity.get("qty", 0) > 0
