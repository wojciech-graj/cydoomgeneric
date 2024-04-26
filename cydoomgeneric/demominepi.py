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
from typing import Optional, Tuple, Set, List

from mcpi import minecraft, block, event
from mcpi.vec3 import Vec3
import numpy as np
from skimage import color

import cydoomgeneric as cdg

PALETTE_BLOCKS = (
    block.STONE,
    block.DIRT,
    block.COBBLESTONE,
    block.WOOD_PLANKS,
    block.BEDROCK,
    block.SAND,
    block.GRAVEL,
    block.Block(block.WOOD.id, 12),
    block.Block(block.WOOD.id, 13),
    block.Block(block.WOOD.id, 14),
    block.LAPIS_LAZULI_BLOCK,
    block.SANDSTONE,
    block.Block(block.SANDSTONE.id, 1),
    block.Block(block.SANDSTONE.id, 2),
    block.WOOL,
    block.Block(block.WOOL.id, 1),
    block.Block(block.WOOL.id, 2),
    block.Block(block.WOOL.id, 3),
    block.Block(block.WOOL.id, 4),
    block.Block(block.WOOL.id, 5),
    block.Block(block.WOOL.id, 6),
    block.Block(block.WOOL.id, 7),
    block.Block(block.WOOL.id, 8),
    block.Block(block.WOOL.id, 9),
    block.Block(block.WOOL.id, 10),
    block.Block(block.WOOL.id, 11),
    block.Block(block.WOOL.id, 12),
    block.Block(block.WOOL.id, 13),
    block.Block(block.WOOL.id, 14),
    block.Block(block.WOOL.id, 15),
    block.GOLD_BLOCK,
    block.IRON_BLOCK,
    block.STONE_SLAB_DOUBLE,
    block.Block(block.STONE_SLAB_DOUBLE.id, 6),
    block.BRICK_BLOCK,
    block.MOSS_STONE,
    block.OBSIDIAN,
    block.DIAMOND_BLOCK,
    block.SNOW_BLOCK,
    block.CLAY,
    block.STONE_BRICK,
    block.Block(block.STONE_BRICK.id, 1),
    block.Block(block.STONE_BRICK.id, 2),
    block.MELON,
    block.NETHERRACK,
    block.Block(block.NETHER_REACTOR_CORE.id, 2),
    block.NETHER_BRICK,
    block.Block(155),  # QUARTZ_BLOCK
    block.Block(155, 1),  # CHISELED_QUARTZ_BLOCK
    block.ICE,
)


PALETTE_LAB = color.rgb2lab(np.array((
    (.492, .492, .492),
    (.526, .378, .263),
    (.482, .482, .482),
    (.615, .500, .309),
    (.328, .328, .328),
    (.859, .828, .628),
    (.516, .485, .483),
    (.401, .318, .195),
    (.179, .113, .048),
    (.810, .809, .789),
    (.114, .279, .650),
    (.851, .822, .617),
    (.846, .816, .606),
    (.862, .831, .634),
    (.870, .870, .870),
    (.918, .500, .214),
    (.748, .296, .788),
    (.407, .545, .831),
    (.761, .709, .110),
    (.232, .739, .187),
    (.852, .516, .607),
    (.261, .261, .261),
    (.620, .649, .649),
    (.154, .458, .586),
    (.507, .211, .768),
    (.152, .201, .604),
    (.336, .201, .108),
    (.218, .302, .095),
    (.642, .176, .159),
    (.105, .091, .091),
    (.977, .927, .308),
    (.860, .860, .860),
    (.655, .655, .655),
    (.625, .625, .625),
    (.575, .392, .341),
    (.407, .476, .407),
    (.079, .072, .117),
    (.383, .860, .837),
    (.941, .985, .985),
    (.622, .645, .693),
    (.479, .479, .479),
    (.449, .467, .416),
    (.466, .466, .466),
    (.554, .572, .141),
    (.436, .213, .206),
    (.075, .075, .137),
    (.175, .088, .104),
    (.926, .914, .887),
    (.910, .896, .863),
    (.682, .799, 1.00),
), dtype=float))


PLATFORM = (
    (-1, 0, -2, block.DIAMOND_BLOCK),
    (-1, 0, -1, block.NETHER_REACTOR_CORE),
    (-1, 0, 0, block.Block(block.WOOL.id, 2)),
    (-1, 0, 1, block.GLASS),
    (0, 0, -2, block.BEDROCK_INVISIBLE),
    (0, 0, -1, block.Block(block.WOOL.id, 13)),
    (0, 0, 0, block.STONE),
    (0, 0, 1, block.Block(block.WOOL.id, 3)),
    (1, 0, -2, block.GOLD_BLOCK),
    (1, 0, -1, block.Block(block.NETHER_REACTOR_CORE.id, 1)),
    (1, 0, 0, block.Block(block.WOOL.id, 14)),
    (1, 0, 1, block.GLASS),
)


KEYPOS = {
    (-1, 0, -2): cdg.Keys.FIRE,
    (1, 0, -2): cdg.Keys.USE,
    (-1, 0, -1): cdg.Keys.ENTER,
    (1, 0, -1): cdg.Keys.ESCAPE,
}


class MinecraftPiDoom:
    def __init__(self) -> None:
        self._mc = minecraft.Minecraft.create()
        self._scale = 5
        self._pressed: Set[int] = set()
        self._read_frame_input = False
        self._inputs: List[Tuple[int, int]] = []

        self._ctrls_pos = Vec3(160 // self._scale, 100 // self._scale - 2, 68 - 6 * self._scale)
        self._mc.setBlocks(0, 0, 0, 256, 128, 128, block.AIR)
        self._mc.setBlocks(
            self._ctrls_pos.x - 2, self._ctrls_pos.y + 1, self._ctrls_pos.z + 2,
            self._ctrls_pos.x + 2, self._ctrls_pos.y + 2, self._ctrls_pos.z - 3,
            block.BEDROCK_INVISIBLE)
        self._mc.setBlocks(
            self._ctrls_pos.x - 1, self._ctrls_pos.y + 1, self._ctrls_pos.z + 1,
            self._ctrls_pos.x + 1, self._ctrls_pos.y + 2, self._ctrls_pos.z - 2,
            block.AIR)
        for blk in PLATFORM:
            self._mc.setBlock(
                self._ctrls_pos.x + blk[0], self._ctrls_pos.y + blk[1], self._ctrls_pos.z + blk[2],
                blk[3])
        self._mc.player.setTilePos(self._ctrls_pos + Vec3(0, 1, 0))

    def draw_frame(self, pix: np.ndarray) -> None:
        for y, x in itertools.product(range(0, 200, self._scale), range(0, 320, self._scale)):
            idx = np.argmin(color.deltaE_cie76(PALETTE_LAB, color.rgb2lab(pix[199 - y, x, [2, 1, 0]] / 255)))
            self._mc.setBlock(x // self._scale, y // self._scale, 0, PALETTE_BLOCKS[idx])
        self._mc.getBlockWithData(0, 0, 0)  # Wait for entire frame to be drawn
        self._read_frame_input = False

    def get_key(self) -> Optional[Tuple[int, int]]:
        if not self._read_frame_input:
            self._read_frame_input = True

            dpos = self._mc.player.getTilePos() - self._ctrls_pos
            cur_pressed = set()
            if dpos.y == 1:
                if dpos.x == -1:
                    cur_pressed.add(cdg.Keys.LEFTARROW)
                elif dpos.x == 1:
                    cur_pressed.add(cdg.Keys.RIGHTARROW)
                if dpos.z == -1:
                    cur_pressed.add(cdg.Keys.UPARROW)
                elif dpos.z == 1:
                    cur_pressed.add(cdg.Keys.DOWNARROW)

            for e in self._mc.events.pollBlockHits():
                if e.type != event.BlockEvent.HIT:
                    continue
                dpos = (*(e.pos - self._ctrls_pos),)
                if dpos in KEYPOS:
                    cur_pressed.add(KEYPOS[dpos])

            self._inputs = ([(0, key) for key in iter(self._pressed - cur_pressed)]
                           + [(1, key) for key in iter(cur_pressed - self._pressed)])
            self._pressed = cur_pressed
        return self._inputs.pop() if self._inputs else None


if __name__ == "__main__":
    g = MinecraftPiDoom()
    cdg.init(320,
             200,
             g.draw_frame,
             g.get_key)
    cdg.main()
