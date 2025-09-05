# 🚀 AutoFleet RL: Autonomous Fleet Management System using Reinforcement Learning

## 📖 Project Description

**AutoFleet RL** is an AI-driven solution designed to optimize the operation of **Autonomous Guided Vehicles (AGVs)** in warehouses. Unlike traditional IoT-dependent fleet management systems, this project leverages **Reinforcement Learning algorithms (DQN, PPO, Actor-Critic)** to enable AGVs to learn optimal paths dynamically without relying on expensive sensors like LiDAR or RFID.

The system integrates:

* 🤖 **Reinforcement Learning** for route optimization and task allocation
* 👁 **Computer Vision** for obstacle detection
* 🏗 **3D simulation (Unity/ML-Agents)** for training and testing
* 🖥 **FastAPI + Streamlit Dashboard** for real-time monitoring
* ☁️ **Cloud deployment** for scalability

This approach improves efficiency, reduces congestion, lowers operational costs, and enhances adaptability in modern warehouse logistics.

---

## 🌟 Key Features

* **Reinforcement Learning–Based Optimization**

  * RL (DQN, PPO) for dynamic route planning and task allocation.
  * Real-time adaptability to congestion and warehouse changes.

* **IoT-Free Design**

  * No dependency on costly IoT infrastructure (LiDAR, RFID, GPS).
  * Lowers hardware cost and complexity.

* **Real-Time Decision-Making**

  * AGVs continuously learn and optimize collision avoidance and delivery routes.
  * Environment-aware navigation without external sensors.

* **3D Simulation & Training**

  * Simulates warehouses in **Unity ML-Agents** for safe model training.
  * Tests AGV navigation, congestion handling, and efficiency.

* **Scalable Dashboard & Cloud Deployment**

  * Interactive **Streamlit/React.js dashboard** with live matrix grid.
  * Cloud-ready for real-time fleet monitoring at scale.

* **Performance Metrics**

  * Tracks utilization, distance traveled, collisions avoided, and task completion rate.
  * Provides continuous insights for refinement.

---

## 📁 File Structure

```bash
fleet_dashboard/
├── backend/
│   ├── app.py               # FastAPI app (REST API endpoints)
│   ├── models.py            # Pydantic models
│   ├── engine/              # Core simulation logic
│   │   ├── __init__.py
│   │   ├── warehouse.py     # Warehouse environment & KPIs
│   │   ├── agv.py           # AGV agent logic
│   │   └── pathfinding.py   # Path planning (A*)
│   └── requirements.txt
├── frontend/
│   ├── dashboard.py         # Streamlit dashboard
│   └── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 🔹 A) Start Backend (FastAPI)

```bash
cd backend
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 🔹 B) Start Frontend (Streamlit)

Open a new terminal:

```bash
cd ../frontend
python -m venv .venv && . .venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py
```

The Streamlit dashboard assumes the backend runs at:
👉 `http://localhost:8000`

---

## 🧭 Usage

* Enter natural-language prompts like:

  ```
  Grid size: 12 rows, 12 columns; 
  AGVs: 2 starting at (0,0) and (11,11); 
  Obstacles: (3,3),(3,4),(4,4); 
  Order O1: pick (1,1) deliver (10,10); Run for 150 steps
  ```

* Watch live **matrix visualization** with AGVs, shelves, obstacles, and tasks.

* Track **metrics** such as tasks completed, collisions avoided, and utilization.

---

## 🔌 API Endpoints

* `POST /reset` — reset the simulation with a config object
* `POST /task` — add a natural-language prompt or structured order
* `POST /step?n=1` — advance simulation by `n` ticks
* `GET /state` — fetch current warehouse state (grid, AGVs, orders)
* `GET /metrics` — fetch current KPIs

---

## 🧠 Extending the Project

You can replace the default A\* planner with **advanced RL algorithms**:

* `engine/warehouse.py` → simulation loop and task allocation
* `engine/agv.py` → AGV decision-making logic
* `engine/pathfinding.py` → pathfinding logic (replace A\* with DQN, PPO, or D\* Lite)

This makes the project flexible to adapt **traditional algorithms** or **deep reinforcement learning**.

---

✨ With this setup, you can **simulate**, **visualize**, and **evaluate** autonomous AGV fleets in warehouses, and extend it with **cutting-edge RL research**.

