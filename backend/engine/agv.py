from typing import List, Tuple, Optional, Deque
from collections import deque

Coord = Tuple[int, int]

class AGV:
    def __init__(self, agv_id: int, start: Coord):
        self.id = agv_id
        self.pos: Coord = start
        self.path: Deque[Coord] = deque()
        self.carrying: Optional[str] = None  # order id if carrying
        self.distance_travelled: int = 0
        self.active_ticks: int = 0

    def set_path(self, path: Optional[List[Coord]]):
        self.path = deque(path or [])
        # First element is current pos; pop it to avoid standing still
        if self.path and self.path[0] == self.pos:
            self.path.popleft()

    def step(self):
        # Idle if no path
        if not self.path:
            return
        nxt = self.path.popleft()
        if nxt != self.pos:
            self.distance_travelled += 1
        self.pos = nxt
        self.active_ticks += 1
