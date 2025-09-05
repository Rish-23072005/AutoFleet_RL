import streamlit as st
import requests
import time
import matplotlib.pyplot as plt

API =  "http://localhost:8000"
st.set_page_config(page_title="AGV Warehouse Dashboard", layout="wide")
st.title("🚗 AGV Warehouse Dashboard")

with st.sidebar:
    st.header("Simulation Controls")
    rows = st.number_input("Rows", 5, 50, 12, 1)
    cols = st.number_input("Cols", 5, 50, 12, 1)
    agv_count = st.number_input("AGV count", 1, 10, 2, 1)
    starts = st.text_input("AGV starts CSV (r,c; r,c)", "0,0; 11,11")
    obstacles = st.text_area("Obstacles CSV (r,c; r,c)", "3,3; 3,4; 4,4")
    max_steps = st.number_input("Max steps", 10, 5000, 300, 10)
    if st.button("Reset Simulation"):
        try:
            start_list = [tuple(map(int, x.split(","))) for x in starts.split(";")]
            obs_list = [tuple(map(int, x.split(","))) for x in obstacles.split(";")] if obstacles.strip() else []
            r = requests.post(f"{API}/reset", json={
                "rows": rows, "cols": cols, "agv_starts": start_list[:agv_count],
                "obstacles": obs_list, "shelves": [], "max_steps": max_steps
            }, timeout=5)
            st.success("Simulation reset!")
        except Exception as e:
            st.error(f"Reset error: {e}")

prompt = st.text_input("Enter task prompt", 
    "Grid size: 12 rows, 12 columns; AGVs: 2 starting at (0,0),(11,11); Obstacles: (3,3),(3,4),(4,4); Order O1: pick (1,1) deliver (10,10)")
colA, colB = st.columns([1,1])
with colA:
    if st.button("Send Prompt"):
        try:
            r = requests.post(f"{API}/task", json={"prompt": prompt}, timeout=5)
            st.success(f"Prompt accepted: {r.json().get('orders', [])}")
        except Exception as e:
            st.error(f"Task error: {e}")
with colB:
    steps_to_run = st.number_input("Run N steps", 1, 500, 50, 1)
    if st.button("Run"):
        try:
            r = requests.post(f"{API}/step", params={"n": int(steps_to_run)}, timeout=5)
            st.success("Ran steps.")
        except Exception as e:
            st.error(f"Run error: {e}")

ph1 = st.empty()
ph2 = st.empty()

def draw_state(state):
    rows, cols = state["rows"], state["cols"]
    fig, ax = plt.subplots(figsize=(6,6))
    # grid
    for r in range(rows+1):
        ax.axhline(r, linewidth=0.5)
    for c in range(cols+1):
        ax.axvline(c, linewidth=0.5)
    # obstacles
    for r,c in state["obstacles"]:
        ax.add_patch(plt.Rectangle((c, r), 1, 1, fill=True, alpha=0.3))
    # shelves (optional)
    for r,c in state["shelves"]:
        ax.add_patch(plt.Rectangle((c, r), 1, 1, fill=False, linestyle="--"))
    # agvs
    for a in state["agvs"]:
        ar, ac = a["pos"]
        ax.plot(ac+0.5, ar+0.5, marker="o", markersize=10)
        ax.text(ac+0.5, ar+0.8, f"AGV {a['id']}", ha="center")
    # orders
    for oid, o in state["orders"].items():
        pr, pc = o["pick"]
        dr, dc = o["drop"]
        ax.text(pc+0.1, pr+0.9, f"P:{oid}", fontsize=8)
        ax.text(dc+0.1, dr+0.1, f"D:{oid}", fontsize=8)
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_title(f"Time={state['time']}")
    st.pyplot(fig)

def draw_metrics(metrics):
    st.metric("Time", metrics["time"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Tasks Done / Total", f"{metrics['tasks_done']} / {metrics['tasks_total']}")
    c2.metric("Collisions", metrics["collisions"])
    c3.metric("Utilization", f"{metrics['utilization']:.2%}")
    st.progress(min(1.0, (metrics["tasks_done"] / max(1, metrics["tasks_total"]))))

# Live loop (polling)
if "running" not in st.session_state:
    st.session_state["running"] = True

run_live = st.toggle("Auto-advance (animate)", value=False)
speed = st.slider("Animation speed (steps/tick)", 1, 10, 1)

while run_live:
    try:
        requests.post(f"{API}/step", params={"n": speed}, timeout=5)
        s = requests.get(f"{API}/state", timeout=5).json()
        m = requests.get(f"{API}/metrics", timeout=5).json()
        with ph1.container():
            st.subheader("Warehouse Matrix")
            draw_state(s)
        with ph2.container():
            st.subheader("KPIs")
            draw_metrics(m)
    except Exception as e:
        st.error(f"Live error: {e}")
        break
    time.sleep(0.7)

# Always show the latest state/metrics at least once
try:
    s = requests.get(f"{API}/state", timeout=5).json()
    m = requests.get(f"{API}/metrics", timeout=5).json()
    with ph1.container():
        st.subheader("Warehouse Matrix")
        draw_state(s)
    with ph2.container():
        st.subheader("KPIs")
        draw_metrics(m)
except Exception:
    st.info("Start the backend to see the live state.")
