from typing import List, Tuple, Optional, Set, Dict
from heapq import heappush, heappop

Coord = Tuple[int, int]

def neighbors(r: int, c: int, rows: int, cols: int):
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def heuristic(a: Coord, b: Coord) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def plan_path(grid_blocked: Set[Coord], rows: int, cols: int, start: Coord, goal: Coord) -> Optional[List[Coord]]:
    """A* path from start to goal avoiding blocked cells in grid_blocked."""
    if start == goal:
        return [start]
    closed: Set[Coord] = set()
    came: Dict[Coord, Optional[Coord]] = {start: None}
    g = {start: 0}
    pq = []
    heappush(pq, (heuristic(start, goal), 0, start))
    while pq:
        _, cost, cur = heappop(pq)
        if cur in closed:
            continue
        if cur == goal:
            # reconstruct
            path = []
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            return list(reversed(path))
        closed.add(cur)
        for nb in neighbors(cur[0], cur[1], rows, cols):
            if nb in grid_blocked:
                continue
            new_g = cost + 1
            if nb not in g or new_g < g[nb]:
                g[nb] = new_g
                came[nb] = cur
                heappush(pq, (new_g + heuristic(nb, goal), new_g, nb))
    return None
