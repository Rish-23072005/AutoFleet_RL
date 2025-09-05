from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from models import ResetConfig, PromptIn, OrderIn
from engine.warehouse import WarehouseSim
import re

app = FastAPI(title="AGV Warehouse API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim = WarehouseSim()
sim.reset(rows=12, cols=12, agv_starts=[(0,0)], obstacles=[], shelves=[], max_steps=300)

def parse_prompt(prompt: str):
    # Basic prompt parser
    cfg = {}
    m = re.search(r"Grid size:\s*(\d+)\s*rows,\s*(\d+)\s*columns", prompt, re.I)
    if m:
        cfg["rows"], cfg["cols"] = int(m.group(1)), int(m.group(2))
    m = re.search(r"AGVs?:\s*(\d+).*?starting at\s*((?:\(\s*\d+\s*,\s*\d+\s*\)\s*,?\s*)+)", prompt, re.I)
    if m:
        count = int(m.group(1))
        starts = re.findall(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", m.group(2))
        starts = [(int(r), int(c)) for r,c in starts][:count]
        cfg["agv_starts"] = starts
    obs = re.findall(r"Obstacles?:\s*((?:\(\s*\d+\s*,\s*\d+\s*\)\s*,?\s*)+)", prompt, re.I)
    if obs:
        pts = re.findall(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", obs[0])
        cfg["obstacles"] = [(int(r), int(c)) for r,c in pts]
    # Orders like: Order O1: pick (1,1) deliver (10,10)
    orders = re.findall(r"Order\s+(\w+):\s*pick\s*\((\d+),(\d+)\)\s*deliver\s*\((\d+),(\d+)\)", prompt, re.I)
    return cfg, [(oid, (int(r1),int(c1)), (int(r2),int(c2))) for oid, r1, c1, r2, c2 in orders]

@app.post("/reset")
def reset(cfg: ResetConfig):
    sim.reset(cfg.rows, cfg.cols, cfg.agv_starts, cfg.obstacles, cfg.shelves, cfg.max_steps)
    return {"ok": True, "state": sim.state()}

@app.post("/task")
def task(inp: PromptIn):
    cfg, orders = parse_prompt(inp.prompt)
    if cfg:
        sim.reset(
            cfg.get("rows", sim.rows),
            cfg.get("cols", sim.cols),
            cfg.get("agv_starts", [a.pos for a in sim.agvs]) or [(0,0)],
            cfg.get("obstacles", list(sim.obstacles)),
            list(sim.shelves),
            sim.max_steps
        )
    for oid, pick, drop in orders:
        sim.add_order(oid, pick, drop)
    return {"ok": True, "prompt": inp.prompt, "orders": [o[0] for o in orders]}

@app.post("/order")
def order(inp: OrderIn):
    sim.add_order(inp.id, inp.pick, inp.drop)
    return {"ok": True}

@app.post("/step")
def step(n: Optional[int] = Query(default=1, ge=1, le=100)):
    sim.step(n or 1)
    return {"ok": True, "state": sim.state(), "metrics": sim.metrics()}

@app.get("/state")
def state():
    return sim.state()

@app.get("/metrics")
def metrics():
    return sim.metrics()
