from core.execution import funding_arb
from core.execution.executor import Executor
from core.exchange.internal_cex import InternalCEX


def test_funding_arb_scan_and_execute():
    quotes = {"BTCUSDT": {"bid": 100, "ask": 101}}
    funding = {"BTCUSDT": 400}
    cfg = {"min_net_edge_bps": 300}
    opps = funding_arb.scan_opportunities(quotes, funding, cfg)
    assert opps and opps[0]["symbol"] == "BTCUSDT"
    exe = Executor(InternalCEX())
    risk_cfg = {"max_notional_per_trade_usd": 2000, "max_leg_latency_ms": 800, "max_slippage_bps": 35}
    res = funding_arb.execute(opps[0], exe, risk_cfg)
    assert res["status"] == "filled"
