//
// Copyright(C) 2023-2024 Wojciech Graj
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// DESCRIPTION:
//	Nil.
//

#ifndef DOOM_GENERIC
#define DOOM_GENERIC

#include <stdlib.h>
#include <stdint.h>

extern uint32_t DOOMGENERIC_RESX;
extern uint32_t DOOMGENERIC_RESY;
extern uint32_t* DG_ScreenBuffer;

void dg_Create(uint32_t resx,
	uint32_t resy,
	void (*pDG_DrawFrame)(),
	void (*pDG_SleepMs)(uint32_t),
	uint32_t (*pDG_GetTicksMs)(),
	int (*pDG_GetKey)(int*, unsigned char*),
	void (*pDG_SetWindowTitle)(const char*));
int dg_main(int argc, char **argv);

extern void (*DG_DrawFrame)();
extern void (*DG_SleepMs)(uint32_t);
extern uint32_t (*DG_GetTicksMs)();
extern int (*DG_GetKey)(int*, unsigned char*);
extern void (*DG_SetWindowTitle)(const char*);

#endif /* DOOM_GENERIC */
