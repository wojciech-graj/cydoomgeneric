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


from libc.stdint cimport uint8_t, uint32_t


cdef extern from "doomgeneric.h":
    cdef uint32_t DOOMGENERIC_RESX
    cdef uint32_t DOOMGENERIC_RESY
    cdef uint32_t *DG_ScreenBuffer

    void dg_Create(uint32_t resx,
         uint32_t resy,
         void (*pDG_Init)(),
         void (*pDG_DrawFrame)(),
         void (*pDG_SleepMs)(uint32_t),
         uint32_t (*pDG_GetTicksMs)(),
         int (*pDG_GetKey)(int*, unsigned char*),
         void (*pDG_SetWindowTitle)(const char*))
    int dg_main(int argc, char **argv)


cdef extern from "doomkeys.h":
    cdef const uint8_t KEY_RIGHTARROW
    cdef const uint8_t KEY_LEFTARROW
    cdef const uint8_t KEY_UPARROW
    cdef const uint8_t KEY_DOWNARROW
    cdef const uint8_t KEY_STRAFE_L
    cdef const uint8_t KEY_STRAFE_R
    cdef const uint8_t KEY_USE
    cdef const uint8_t KEY_FIRE
    cdef const uint8_t KEY_ESCAPE
    cdef const uint8_t KEY_ENTER
    cdef const uint8_t KEY_TAB
    cdef const uint8_t KEY_F1
    cdef const uint8_t KEY_F2
    cdef const uint8_t KEY_F3
    cdef const uint8_t KEY_F4
    cdef const uint8_t KEY_F5
    cdef const uint8_t KEY_F6
    cdef const uint8_t KEY_F7
    cdef const uint8_t KEY_F8
    cdef const uint8_t KEY_F9
    cdef const uint8_t KEY_F10
    cdef const uint8_t KEY_F11
    cdef const uint8_t KEY_F12

    cdef const uint8_t KEY_BACKSPACE
    cdef const uint8_t KEY_PAUSE

    cdef const uint8_t KEY_EQUALS
    cdef const uint8_t KEY_MINUS

    cdef const uint8_t KEY_RSHIFT
    cdef const uint8_t KEY_RCTRL
    cdef const uint8_t KEY_RALT

    cdef const uint8_t KEY_LALT

    cdef const uint8_t KEY_CAPSLOCK
    cdef const uint8_t KEY_NUMLOCK
    cdef const uint8_t KEY_SCRLCK
    cdef const uint8_t KEY_PRTSCR

    cdef const uint8_t KEY_HOME
    cdef const uint8_t KEY_END
    cdef const uint8_t KEY_PGUP
    cdef const uint8_t KEY_PGDN
    cdef const uint8_t KEY_INS
    cdef const uint8_t KEY_DEL

    cdef const uint8_t KEYP_0
    cdef const uint8_t KEYP_1
    cdef const uint8_t KEYP_2
    cdef const uint8_t KEYP_3
    cdef const uint8_t KEYP_4
    cdef const uint8_t KEYP_5
    cdef const uint8_t KEYP_6
    cdef const uint8_t KEYP_7
    cdef const uint8_t KEYP_8
    cdef const uint8_t KEYP_9

    cdef const uint8_t KEYP_DIVIDE
    cdef const uint8_t KEYP_PLUS
    cdef const uint8_t KEYP_MINUS
    cdef const uint8_t KEYP_MULTIPLY
    cdef const uint8_t KEYP_PERIOD
    cdef const uint8_t KEYP_EQUALS
    cdef const uint8_t KEYP_ENTER
