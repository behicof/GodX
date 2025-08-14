class RiskManager:
    """Very small placeholder risk manager."""

    def check(self, opportunity: dict) -> bool:
        """Approve trade if all quantities are positive."""
        if "legs" in opportunity:
            return all(leg.get("qty", 0) > 0 for leg in opportunity["legs"])
        return opportunity.get("qty", 0) > 0
