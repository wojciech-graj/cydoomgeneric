"""
 Copyright(C) 2024 Wojciech Graj

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
"""

from enum import IntEnum
from typing import Any, Callable, Literal, Optional, Sequence

import numpy as np

def init(resx: int,
         resy: int,
         draw_frame: Callable[
             [np.ndarray[tuple[Any, Any, Literal[4]],
                         np.dtype[np.uint8]]], None],
         get_key: Callable[[], Optional[tuple[int, int]]],
         sleep_ms: Optional[Callable[[int], None]] = None,
         get_ticks_ms: Optional[Callable[[], int]] = None,
         set_window_title: Optional[Callable[[str], None]] = None) -> None:
    ...


def main(argv: Optional[Sequence[str]] = None) -> int:
    ...


class Keys(IntEnum):
    RIGHTARROW: int
    LEFTARROW: int
    UPARROW: int
    DOWNARROW: int
    STRAFE_L: int
    STRAFE_R: int
    USE: int
    FIRE: int
    ESCAPE: int
    ENTER: int
    TAB: int
    F1: int
    F2: int
    F3: int
    F4: int
    F5: int
    F6: int
    F7: int
    F8: int
    F9: int
    F10: int
    F11: int
    F12: int

    BACKSPACE: int
    PAUSE: int

    EQUALS: int
    MINUS: int

    RSHIFT: int
    RCTRL: int
    RALT: int

    LALT: int

    CAPSLOCK: int
    NUMLOCK: int
    SCRLCK: int
    PRTSCR: int

    HOME: int
    END: int
    PGUP: int
    PGDN: int
    INS: int
    DEL: int

    P_0: int
    P_1: int
    P_2: int
    P_3: int
    P_4: int
    P_5: int
    P_6: int
    P_7: int
    P_8: int
    P_9: int

    P_DIVIDE: int
    P_PLUS: int
    P_MINUS: int
    P_MULTIPLY: int
    P_PERIOD: int
    P_EQUALS: int
    P_ENTER: int
