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

import itertools
from typing import Optional, Tuple, List

import numpy as np
import uno

import cydoomgeneric as cdg


# Change this variable to adjust screen resolution. Allowed values in range [0,5]
SCALE = 1


KEYMAP = {
    'a': cdg.Keys.LEFTARROW,
    'd': cdg.Keys.RIGHTARROW,
    'w': cdg.Keys.UPARROW,
    's': cdg.Keys.DOWNARROW,
    ',': cdg.Keys.STRAFE_L,
    '.': cdg.Keys.STRAFE_R,
    'e': cdg.Keys.FIRE,
    ' ': cdg.Keys.USE,
    'm': cdg.Keys.RSHIFT,
    'r': cdg.Keys.ENTER,
    '`': cdg.Keys.ESCAPE,
}


GRAD = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


class CalcDoom:
    def __init__(self, sheet, scale) -> None:
        self._scale = scale
        self._resx = 320 // (2 ** scale)
        self._resy = 200 // (2 ** scale)
        self._image_cell = sheet.getCellByPosition(1, 0)
        self._input_cell = sheet.getCellByPosition(0, 0)
        self._input: Optional[List[str]] = None
        self._pressed: List[int] = []
        self._pressed_prev: List[int] = []


    def init(self) -> None:
        for y in range(1, self._resy + 1):
            print(f"Initializing row {y}/{self._resy}")
            for x in range(1, self._resx + 1):
                cell = sheet.getCellByPosition(x, y)
                cell.setFormula(f"=MID(B1;{x + (y - 1) * self._resx};1)")


    def draw_frame(self, pix) -> None:
        pix = np.average(pix, axis=-1)
        self._image_cell.setString(''.join(
            [GRAD[int(pix[y, x] * 0.35)] for y, x in
                itertools.product(range(0, 200, 2 ** self._scale), range(0, 320, 2 ** self._scale))]))


    def get_key(self) -> Optional[Tuple[int, int]]:
        if len(self._pressed) > 0:
            return (0, self._pressed.pop())
        if self._input is None:
            self._input = list(self._input_cell.getString().lower())
            self._input_cell.setString("")
        if len(self._input) == 0:
            self._input = None
            self._pressed = self._pressed_prev
            self._pressed_prev = []
            return None
        c = self._input.pop()
        key = KEYMAP[c] if c in KEYMAP else ord(c)
        self._pressed_prev.append(key)
        return (1, key)


if __name__ == "__main__":
    local_ctx = uno.getComponentContext()
    smgr_local = local_ctx.ServiceManager
    resolver = smgr_local.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local_ctx)
    uno_ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002,tcpNoDelay=1;urp;StarOffice.ComponentContext")
    uno_smgr = uno_ctx.ServiceManager

    desktop = uno_smgr.createInstanceWithContext("com.sun.star.frame.Desktop", uno_ctx)
    PropertyValue = uno.getClass('com.sun.star.beans.PropertyValue')
    document = desktop.loadComponentFromURL("private:factory/scalc", "_blank", 0, (PropertyValue(),))
    sheet = document.getSheets()[0]

    g = CalcDoom(sheet, SCALE)
    cdg.init(320,
        200,
        g.draw_frame,
        g.get_key,
        init=g.init)
    cdg.main()
