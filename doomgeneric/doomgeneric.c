//
// Copyright(C) 1993-1996 Id Software, Inc.
// Copyright(C) 2005-2014 Simon Howard
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

#include "doomgeneric.h"

#include <stdio.h>

#include "m_argv.h"

void D_DoomMain (void);
void M_FindResponseFile(void);

uint32_t DOOMGENERIC_RESX;
uint32_t DOOMGENERIC_RESY;
uint32_t* DG_ScreenBuffer = 0;

void (*DG_DrawFrame)();
void (*DG_SleepMs)(uint32_t);
uint32_t (*DG_GetTicksMs)();
int (*DG_GetKey)(int*, unsigned char*);
void (*DG_SetWindowTitle)(const char*);

void dg_Create(uint32_t resx,
	uint32_t resy,
	void (*pDG_DrawFrame)(),
	void (*pDG_SleepMs)(uint32_t),
	uint32_t (*pDG_GetTicksMs)(),
	int (*pDG_GetKey)(int*, unsigned char*),
	void (*pDG_SetWindowTitle)(const char*))
{
	DOOMGENERIC_RESX = resx;
	DOOMGENERIC_RESY = resy;

	DG_DrawFrame = pDG_DrawFrame;
	DG_SleepMs = pDG_SleepMs;
	DG_GetTicksMs = pDG_GetTicksMs;
	DG_GetKey = pDG_GetKey;
	DG_SetWindowTitle = pDG_SetWindowTitle;

	DG_ScreenBuffer = malloc(DOOMGENERIC_RESX * DOOMGENERIC_RESY * 4);
}

int dg_main(int argc, char **argv)
{
    // save arguments

    myargc = argc;
    myargv = argv;

    M_FindResponseFile();

    // start doom
    printf("Starting D_DoomMain\r\n");

	D_DoomMain ();

    return 0;
}
