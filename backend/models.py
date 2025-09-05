from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Optional

Coord = Tuple[int, int]

class ResetConfig(BaseModel):
    rows: int = 12
    cols: int = 12
    agv_starts: List[Coord] = Field(default_factory=lambda: [(0,0)])
    obstacles: List[Coord] = Field(default_factory=list)
    shelves: List[Coord] = Field(default_factory=list)
    max_steps: int = 300

class PromptIn(BaseModel):
    prompt: str

class OrderIn(BaseModel):
    id: str
    pick: Coord
    drop: Coord

class StepQuery(BaseModel):
    n: int = 1
