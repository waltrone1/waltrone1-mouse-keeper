from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass

IS_WINDOWS = os.name == 'nt'


class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]


@dataclass
class MousePoint:
    x: int
    y: int


class MouseController:
    def __init__(self) -> None:
        self.supported = IS_WINDOWS
        if self.supported:
            self.user32 = ctypes.windll.user32
        else:
            self.user32 = None

    def get_position(self) -> MousePoint:
        if not self.supported:
            return MousePoint(0, 0)
        point = POINT()
        self.user32.GetCursorPos(ctypes.byref(point))
        return MousePoint(point.x, point.y)

    def set_position(self, x: int, y: int) -> None:
        if not self.supported:
            return
        self.user32.SetCursorPos(int(x), int(y))

    def nudge(self, distance: int = 1) -> MousePoint:
        origin = self.get_position()
        self.set_position(origin.x + max(1, distance), origin.y)
        return origin

    def restore(self, point: MousePoint) -> None:
        self.set_position(point.x, point.y)

    def left_click(self) -> None:
        if not self.supported:
            return
        self.user32.mouse_event(0x0002, 0, 0, 0, 0)
        self.user32.mouse_event(0x0004, 0, 0, 0, 0)
