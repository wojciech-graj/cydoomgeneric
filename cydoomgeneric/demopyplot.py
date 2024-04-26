"""
 Copyright(C) 2023-2024 Wojciech Graj

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
"""


import sys
from typing import Optional, Tuple, List

import matplotlib.pyplot as plt
import numpy as np

import cydoomgeneric as cdg


KEYMAP = {
    "left": cdg.Keys.LEFTARROW,
    "right": cdg.Keys.RIGHTARROW,
    "up": cdg.Keys.UPARROW,
    "down": cdg.Keys.DOWNARROW,
    ',': cdg.Keys.STRAFE_L,
    '.': cdg.Keys.STRAFE_R,
    "control": cdg.Keys.FIRE,
    "space": cdg.Keys.USE,
    "shift": cdg.Keys.RSHIFT,
    "enter": cdg.Keys.ENTER,
    "escape": cdg.Keys.ESCAPE,
}


class PyPlotDoom:
    def __init__(self) -> None:
        self._keyevent_queue: List[Tuple[str, int]] = []
        self._fig = plt.figure()
        self._ax = self._fig.add_subplot(1,1,1)
        self._fig.canvas.mpl_connect('key_press_event', self._on_press)
        self._fig.canvas.mpl_connect('key_release_event', self._on_release)
        self._fig.canvas.mpl_connect('close_event', lambda _: sys.exit())
        self._fig.show()

    def _on_press(self, event) -> None:
        self._keyevent_queue.append((event.key, 1))

    def _on_release(self, event) -> None:
        self._keyevent_queue.append((event.key, 0))

    def draw_frame(self, pixels: np.ndarray) -> None:
        self._ax.clear()
        self._ax.imshow(pixels[:,:,[2,1,0]])
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def get_key(self) -> Optional[Tuple[int, int]]:
        if len(self._keyevent_queue) == 0:
            return None
        (key, pressed) = self._keyevent_queue.pop(0)
        if key in KEYMAP:
            return (pressed, KEYMAP[key])
        if len(key) == 1:
            return (pressed, ord(key.lower()))
        return self.get_key()

    def set_window_title(self, t: str) -> None:
        self._fig.suptitle(t)


if __name__ == "__main__":
    g = PyPlotDoom()
    cdg.init(640,
        400,
        g.draw_frame,
        g.get_key,
        set_window_title=g.set_window_title)
    cdg.main()
