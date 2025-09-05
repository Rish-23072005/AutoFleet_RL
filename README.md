# Fleet Dashboard (AGV Warehouse) — FastAPI + Streamlit

A production-ready template to run a dynamic, motion-based AGV warehouse dashboard with:

- **Backend**: FastAPI (simulation engine, REST API)
- **Frontend**: Streamlit (live dashboard, matrix grid, controls, metrics)

## 1) File structure

```bash
fleet_dashboard/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── warehouse.py
│   │   ├── agv.py
│   │   └── pathfinding.py
│   └── requirements.txt
├── frontend/
│   ├── dashboard.py
│   └── requirements.txt
└── README.md
```

## 2) Quick start

### A) Start backend (FastAPI)

```bash
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### B) Start frontend (Streamlit)

Open a new terminal:

```bash
cd ../frontend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py
```

The Streamlit dashboard assumes the backend is at `http://localhost:8000`.

## 3) Features

- Enter natural-language prompts like:  
  `Grid size: 12 rows, 12 columns; AGVs: 2 starting at (0,0) and (11,11); Obstacles: (3,3),(3,4),(4,4); Order O1: pick (1,1) deliver (10,10); Run for 150 steps`
- Live matrix grid visualization with shelves/obstacles, AGV motion, order status.
- Metrics: steps, distance, tasks completed, collisions avoided, utilization.

## 4) API

- `POST /reset` — reset the simulation with a config object (or minimal defaults).
- `POST /task` — add a natural-language prompt or structured order.
- `POST /step?n=1` — advance simulation by n ticks.
- `GET /state` — current warehouse state (grid, AGVs, orders).
- `GET /metrics` — current KPIs.

## 5) Adapting your RL engine

Replace logic inside `engine/*.py` with your RL planner (DQN, D* Lite, etc.).
Keep function signatures stable so the API remains compatible.

```python
# engine/warehouse.py -> WarehouseSim (step(), add_order(), add_agv(), reset())
# engine/agv.py       -> AGV (decide_next_move(state), move_to(next_pos))
# engine/pathfinding.py -> plan_path(grid, start, goal)
```
