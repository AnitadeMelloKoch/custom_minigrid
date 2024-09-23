from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import numpy as np

from minigrid.core.constants import (
    COLOR_TO_IDX,
    COLORS,
    IDX_TO_COLOR,
    IDX_TO_OBJECT,
    OBJECT_TO_IDX,
)
from minigrid.utils.rendering import (
    fill_coords,
    point_in_circle,
    point_in_line,
    point_in_rect,
)

if TYPE_CHECKING:
    from minigrid.minigrid_env import MiniGridEnv

Point = Tuple[int, int]

from minigrid.core.world_object import Door, Key

class CustomDoor(Door):
    def __init__(self, 
                 color: str, 
                 is_open: bool = False, 
                 is_locked: bool = False):
        super().__init__(color, is_open, is_locked)
    
    def toggle(self, env, pos):
        # if player is holding right key can open door
        if self.is_locked:
            if any((isinstance(obj, Key) and obj.color == self.color) for obj in env.carrying):
                self.is_locked = False
                self.is_open = True
                return True
            return False
        
        self.is_open = not self.is_open
        return True
    
class CustomKey(Key):
    def __init__(self, color: str = "blue"):
        super().__init__(color)
    
    def can_overlap(self) -> bool:
        return False

