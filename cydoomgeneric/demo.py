"""
 Copyright(C) 2023 Wojciech Graj

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
import time
from typing import Optional, Tuple


import cydoomgeneric as cdg
import matplotlib.pyplot as plt
import numpy as np


keymap = {
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
    def on_press(self, event) -> None:
        self.keyevent_queue.append((event.key, 1))


    def on_release(self, event) -> None:
        self.keyevent_queue.append((event.key, 0))


    def init(self) -> None:
        self.keyevent_queue = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_release)
        self.fig.canvas.mpl_connect('close_event', sys.exit)
        self.fig.show()


    def draw_frame(self, pixels: np.ndarray) -> None:
        self.ax.clear()
        self.ax.imshow(pixels[:,:,[2,1,0]])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def get_key(self) -> Optional[Tuple[int, int]]:
        if len(self.keyevent_queue) == 0:
            return None
        (key, pressed) = self.keyevent_queue.pop(0)
        if key in keymap:
            return (pressed, keymap[key])
        elif len(key) == 1:
            return (pressed, ord(key.lower()))
        return (0, 0)


    def set_window_title(self, t: str) -> None:
        self.fig.suptitle(t)


if __name__ == "__main__":
    g = PyPlotDoom()
    cdg.init(640,
        400,
        g.draw_frame,
        g.get_key,
        init=g.init,
        set_window_title=g.set_window_title)
    cdg.main()
