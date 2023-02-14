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


from enum import IntEnum
import time
from typing import Callable, Optional, Tuple, Sequence, NoReturn


from cpython.mem cimport PyMem_Malloc, PyMem_Free
cimport cydoomgeneric as cdg
import numpy as np
cimport numpy as np


__init_f: Optional[Callable[None, None]]
__draw_frame_f: Callable[[np.ndarray], None]
__sleep_ms_f: Optional[Callable[[int], None]]
__get_ticks_ms_f: Optional[Callable[None, int]]
__get_key_f: Callable[None, Optional[Tuple[int, int]]]
__set_window_title_f: Optional[Callable[[str], None]]
__start_time: int


cdef void __init():
    if __init_f:
        __init_f()


cdef void __draw_frame():
    __draw_frame_f(np.asarray(<uint8_t[:cdg.DOOMGENERIC_RESY, :cdg.DOOMGENERIC_RESX, :4]><uint8_t*>&cdg.DG_ScreenBuffer[0]))


cdef void __sleep_ms(uint32_t ms):
    if __sleep_ms_f:
        __sleep_ms_f(ms)
    else:
        time.sleep(ms / 1000)


cdef uint32_t __get_ticks_ms():
    if __get_ticks_ms_f:
        return __get_ticks_ms_f()
    else:
        return (time.time() - __start_time) * 1000


cdef int __get_key(int *pressed, unsigned char *key):
    r = __get_key_f()
    if r is None:
        return 0
    (pressed[0], key[0]) = r
    return 1


cdef void __set_window_title(const char *title):
    if __set_window_title_f:
        __set_window_title_f(title.decode("utf-8"))


def init(resx: int,
    resy: int,
    draw_frame: Callable[[np.ndarray], None],
    get_key: Callable[[int], str],
    init: Optional[Callable[None, None]]=None,
    sleep_ms: Optional[Callable[[int], None]]=None,
    get_ticks_ms: Optional[Callable[None, int]]=None,
    set_window_title: Optional[Callable[[str], None]]=None
    ) -> None:
    """
    init(resx, resx, init, draw_frame, sleep_ms, get_ticks_ms, get_key, set_window_title) -> None

    Initializes the doom context.

    :param int resx:
    :param int resy:
    :param Callable[[np.ndarray], None] draw_frame: Called every frame. Takes framebuffer as np.ndarray in shape [resy, resx, 4]. Pixels are BGR.
    :param Callable[[int], Optional[Tuple[int, int]]] get_key: Called multiple times every frame until input is exhausted. Return None when input is exhausted. Otherwise, return (is pressed ~0/1~, key).
    :param Optional[Callable[None, None]] init: Initialization function called immediately after this function terminates
    :param Optional[Callable[[int], None]] sleep_ms:
    :param Optional[Callable[None, int]] get_ticks_ms:
    :param Optional[Callable[[str], None]] set_window_title:
    """
    global __init_f
    global __draw_frame_f
    global __sleep_ms_f
    global __get_ticks_ms_f
    global __get_key_f
    global __set_window_title_f
    global __start_time

    __init_f = init
    __draw_frame_f = draw_frame
    __sleep_ms_f = sleep_ms
    __get_ticks_ms_f = get_ticks_ms
    __get_key_f = get_key
    __set_window_title_f = set_window_title
    __start_time = time.time()

    cdg.dg_Create(resx,
        resy,
        &__init,
        &__draw_frame,
        &__sleep_ms,
        &__get_ticks_ms,
        &__get_key,
        &__set_window_title)


def main(argv: Optional[Sequence[str]]=None) -> int:
    """
    main(argv) -> int

    Run doom. Must be called after init.

    :param Optional[Sequence[str]] argv:
    """
    if argv is None:
        return cdg.dg_main(0, NULL)

    bytestrings = []
    cdef char **cargv = <char**>PyMem_Malloc(sizeof(char *) * len(argv))
    for i, a in enumerate(argv):
        bs = bytes(a, "utf-8")
        bytestrings.append(bs)
        cargv[i] = bs
    rval = cdg.dg_main(len(argv), cargv)
    PyMem_Free(cargv)
    return rval


class Keys(IntEnum):
    RIGHTARROW = cdg.KEY_RIGHTARROW
    LEFTARROW = cdg.KEY_LEFTARROW
    UPARROW = cdg.KEY_UPARROW
    DOWNARROW = cdg.KEY_DOWNARROW
    STRAFE_L = cdg.KEY_STRAFE_L
    STRAFE_R = cdg.KEY_STRAFE_R
    USE = cdg.KEY_USE
    FIRE = cdg.KEY_FIRE
    ESCAPE = cdg.KEY_ESCAPE
    ENTER = cdg.KEY_ENTER
    TAB = cdg.KEY_TAB
    F1 = cdg.KEY_F1
    F2 = cdg.KEY_F2
    F3 = cdg.KEY_F3
    F4 = cdg.KEY_F4
    F5 = cdg.KEY_F5
    F6 = cdg.KEY_F6
    F7 = cdg.KEY_F7
    F8 = cdg.KEY_F8
    F9 = cdg.KEY_F9
    F10 = cdg.KEY_F10
    F11 = cdg.KEY_F11
    F12 = cdg.KEY_F12

    BACKSPACE = cdg.KEY_BACKSPACE
    PAUSE = cdg.KEY_PAUSE

    EQUALS = cdg.KEY_EQUALS
    MINUS = cdg.KEY_MINUS

    RSHIFT = cdg.KEY_RSHIFT
    RCTRL = cdg.KEY_RCTRL
    RALT = cdg.KEY_RALT

    LALT = cdg.KEY_LALT

    CAPSLOCK = cdg.KEY_CAPSLOCK
    NUMLOCK = cdg.KEY_NUMLOCK
    SCRLCK = cdg.KEY_SCRLCK
    PRTSCR = cdg.KEY_PRTSCR

    HOME = cdg.KEY_HOME
    END = cdg.KEY_END
    PGUP = cdg.KEY_PGUP
    PGDN = cdg.KEY_PGDN
    INS = cdg.KEY_INS
    DEL = cdg.KEY_DEL

    P_0 = cdg.KEYP_0
    P_1 = cdg.KEYP_1
    P_2 = cdg.KEYP_2
    P_3 = cdg.KEYP_3
    P_4 = cdg.KEYP_4
    P_5 = cdg.KEYP_5
    P_6 = cdg.KEYP_6
    P_7 = cdg.KEYP_7
    P_8 = cdg.KEYP_8
    P_9 = cdg.KEYP_9

    P_DIVIDE = cdg.KEYP_DIVIDE
    P_PLUS = cdg.KEYP_PLUS
    P_MINUS = cdg.KEYP_MINUS
    P_MULTIPLY = cdg.KEYP_MULTIPLY
    P_PERIOD = cdg.KEYP_PERIOD
    P_EQUALS = cdg.KEYP_EQUALS
    P_ENTER = cdg.KEYP_ENTER
