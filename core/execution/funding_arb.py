from typing import List, Dict
from core.execution.executor import Executor

def net_edge_bps(funding_recv_bps:float, fees_bps:float, borrow_bps:float, slip_bps:float, fx_bps:float)->float:
    return funding_recv_bps - (fees_bps + borrow_bps + slip_bps + fx_bps)

def scan_opportunities(quotes:Dict, funding:Dict, cfg:Dict)->List[Dict]:
    out=[]
    theta=cfg["thresholds"]["funding_arb"]["min_net_edge_bps"]
    slip=cfg["thresholds"]["funding_arb"]["max_slippage_bps"]
    for sym, info in funding.items():
        edge = net_edge_bps(info["funding_bps"], fees_bps=6, borrow_bps=0, slip_bps=slip, fx_bps=0)
        if edge>=theta: out.append({"symbol":sym,"edge_bps":edge})
    return out

def execute(opp:Dict, exe:Executor, cfg:Dict)->Dict:
    sym=opp["symbol"]; q=cfg["quotes"][sym]
    leg1={"side":"BUY","symbol":sym,"px":q["spot"]}
    leg2={"side":"SELL","symbol":sym,"px":q["perp"]}
    return exe.place_ioc_pair(leg1, leg2,
        max_latency_ms=cfg["thresholds"]["funding_arb"]["max_leg_latency_ms"],
        max_slippage_bps=cfg["thresholds"]["funding_arb"]["max_slippage_bps"])
