from dataclasses import dataclass
from core.data.logger import logger


@dataclass
class RiskCfg:
    """Risk thresholds in USD."""
    max_notional_usd: float = float("inf")
    max_sym_exposure_usd: float = float("inf")
    max_exposure_usd: float = float("inf")

    @classmethod
    def from_dict(cls, cfg: dict) -> "RiskCfg":
        """Create config from dictionary values."""
        return cls(
            max_notional_usd=cfg.get("max_notional_usd", float("inf")),
            max_sym_exposure_usd=cfg.get("max_sym_exposure_usd", float("inf")),
            max_exposure_usd=cfg.get("max_exposure_usd", float("inf")),
        )


class RiskManager:
    """Evaluate trades against configured thresholds."""

    def __init__(self, cfg: dict | RiskCfg):
        self.cfg = cfg if isinstance(cfg, RiskCfg) else RiskCfg.from_dict(cfg or {})

    def check(
        self,
        symbol: str,
        notional_usd: float,
        sym_exposure_usd: float,
        ex_exposure_usd: float,
    ) -> tuple[bool, str]:
        """Return (allowed, reason) for a proposed trade."""
        if notional_usd > self.cfg.max_notional_usd:
            reason = (
                f"notional {notional_usd} exceeds limit {self.cfg.max_notional_usd}"
            )
            logger.warning(f"risk_reject symbol={symbol} reason={reason}")
            return False, reason
        if sym_exposure_usd > self.cfg.max_sym_exposure_usd:
            reason = (
                f"symbol exposure {sym_exposure_usd} exceeds limit {self.cfg.max_sym_exposure_usd}"
            )
            logger.warning(f"risk_reject symbol={symbol} reason={reason}")
            return False, reason
        if ex_exposure_usd > self.cfg.max_exposure_usd:
            reason = (
                f"exchange exposure {ex_exposure_usd} exceeds limit {self.cfg.max_exposure_usd}"
            )
            logger.warning(f"risk_reject symbol={symbol} reason={reason}")
            return False, reason
        return True, "ok"
