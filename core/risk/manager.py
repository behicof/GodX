from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Union

from core.data.logger import logger


@dataclass
class RiskCfg:
    """Configuration for :class:`RiskManager`. Limits are denominated in USD."""

    trade_limit_usd: float = float("inf")
    """Maximum notional allowed per trade."""

    symbol_limit_usd: float = float("inf")
    """Maximum aggregated exposure allowed per symbol."""

    exchange_limit_usd: float = float("inf")
    """Maximum aggregated exposure allowed per exchange."""


class RiskManager:
    """Simple risk manager supporting basic notional checks."""

    TRADE_LIMIT = "TRADE_LIMIT"
    SYMBOL_LIMIT = "SYMBOL_LIMIT"
    EXCHANGE_LIMIT = "EXCHANGE_LIMIT"

    def __init__(self, cfg: Union[RiskCfg, Dict] | None = None):
        if cfg is None:
            cfg = RiskCfg()
        elif isinstance(cfg, dict):
            cfg = RiskCfg(**cfg)
        self.cfg = cfg

    def check(
        self,
        symbol: str,
        notional_usd: float,
        sym_exposure_usd: float,
        ex_exposure_usd: float,
    ) -> Tuple[bool, str | None]:
        """Validate order against configured limits.

        Returns a tuple of ``(approved, reason)`` where ``reason`` is ``None`` when
        the trade is approved or one of ``TRADE_LIMIT``, ``SYMBOL_LIMIT`` or
        ``EXCHANGE_LIMIT`` when rejected.
        """

        if notional_usd > self.cfg.trade_limit_usd:
            reason = self.TRADE_LIMIT
            logger.info(
                f"risk_reject symbol={symbol} reason={reason} notional={notional_usd}"
            )
            return False, reason

        if sym_exposure_usd + notional_usd > self.cfg.symbol_limit_usd:
            reason = self.SYMBOL_LIMIT
            logger.info(
                f"risk_reject symbol={symbol} reason={reason} sym_exp={sym_exposure_usd} notional={notional_usd}"
            )
            return False, reason

        if ex_exposure_usd + notional_usd > self.cfg.exchange_limit_usd:
            reason = self.EXCHANGE_LIMIT
            logger.info(
                f"risk_reject symbol={symbol} reason={reason} ex_exp={ex_exposure_usd} notional={notional_usd}"
            )
            return False, reason

        return True, None
