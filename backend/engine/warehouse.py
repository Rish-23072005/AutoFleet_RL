from typing import List, Tuple, Dict, Optional, Set
from .agv import AGV
from .pathfinding import plan_path

Coord = Tuple[int, int]

class Order:
    def __init__(self, oid: str, pick: Coord, drop: Coord):
        self.id = oid
        self.pick = pick
        self.drop = drop
        self.status = "pending"  # pending -> picking -> delivering -> done

class WarehouseSim:
    def __init__(self, rows: int = 12, cols: int = 12):
        self.rows = rows
        self.cols = cols
        self.obstacles: Set[Coord] = set()
        self.shelves: Set[Coord] = set()
        self.agvs: List[AGV] = []
        self.orders: Dict[str, Order] = {}
        self.time = 0
        self.max_steps = 300
        # KPIs
        self.collisions = 0

    def reset(self, rows: int, cols: int, agv_starts: List[Coord], obstacles: List[Coord], shelves: List[Coord], max_steps: int = 300):
        self.__init__(rows, cols)
        self.obstacles = set(map(tuple, obstacles))
        self.shelves = set(map(tuple, shelves))
        self.max_steps = max_steps
        self.agvs = [AGV(i+1, tuple(start)) for i, start in enumerate(agv_starts)]
        self.orders = {}
        self.time = 0
        self.collisions = 0

    def add_order(self, oid: str, pick: Coord, drop: Coord):
        self.orders[oid] = Order(oid, tuple(pick), tuple(drop))

    def plan(self):
        """Very simple dispatcher: assign each idle AGV the oldest pending task stage."""
        blocked = set(self.obstacles) | {agv.pos for agv in self.agvs}
        for agv in self.agvs:
            if agv.path:
                continue  # already en route
            # Find a target based on order stage
            target: Optional[Coord] = None
            assigned_order: Optional[Order] = None
            for order in self.orders.values():
                if order.status == "pending":
                    target = order.pick
                    assigned_order = order
                    break
                elif order.status == "picking":
                    target = order.drop
                    assigned_order = order
                    break
            if target is None:
                continue
            path = plan_path(blocked - {agv.pos}, self.rows, self.cols, agv.pos, target)
            agv.set_path(path)
            if assigned_order and order.status == "pending":
                order.status = "picking"

    def resolve_collisions(self):
        positions: Dict[Coord, List[AGV]] = {}
        for agv in self.agvs:
            positions.setdefault(agv.pos, []).append(agv)
        for pos, lst in positions.items():
            if len(lst) > 1:
                self.collisions += len(lst) - 1  # count overlaps
                # simple resolution: push all but one back by undoing last step
                survivor = lst[0]
                for loser in lst[1:]:
                    # No movement this tick for loser (simulate wait)
                    loser.path.appendleft(loser.pos)

    def step(self, n: int = 1):
        for _ in range(n):
            if self.time >= self.max_steps:
                break
            # Re-plan if necessary
            self.plan()
            # Move
            for agv in self.agvs:
                agv.step()
            # Handle task completions
            for order in self.orders.values():
                if order.status == "picking":
                    # if any agv reached pick, set to delivering
                    if any(agv.pos == order.pick for agv in self.agvs):
                        order.status = "delivering"
                elif order.status == "delivering":
                    if any(agv.pos == order.drop for agv in self.agvs):
                        order.status = "done"
            # Simple collision logic after movement
            self.resolve_collisions()
            self.time += 1

    def state(self) -> Dict:
        return {
            "time": self.time,
            "rows": self.rows,
            "cols": self.cols,
            "obstacles": list(map(list, self.obstacles)),
            "shelves": list(map(list, self.shelves)),
            "agvs": [{"id": a.id, "pos": list(a.pos), "active_ticks": a.active_ticks, "dist": a.distance_travelled} for a in self.agvs],
            "orders": {oid: {"pick": list(o.pick), "drop": list(o.drop), "status": o.status} for oid, o in self.orders.items()},
        }

    def metrics(self) -> Dict:
        total_ticks = max(1, self.time)
        total_possible = len(self.agvs) * total_ticks
        active = sum(a.active_ticks for a in self.agvs)
        utilization = active / total_possible
        done = sum(1 for o in self.orders.values() if o.status == "done")
        return {
            "time": self.time,
            "tasks_total": len(self.orders),
            "tasks_done": done,
            "collisions": self.collisions,
            "distance_total": sum(a.distance_travelled for a in self.agvs),
            "utilization": utilization,
        }
