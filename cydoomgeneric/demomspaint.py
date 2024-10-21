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

import subprocess
import time
from typing import Optional

import numpy as np
import pyautogui
import pywinctl as pwc
from skimage import color, filters, measure, morphology, segmentation

import cydoomgeneric as cdg

PAINT_COMMAND = ["wine", "mspaint"]

PALETTE_LAB = color.rgb2lab(
    np.array((
        (0, 0, 0),
        (128, 128, 128),
        (128, 0, 0),
        (128, 128, 0),
        (0, 128, 0),
        (0, 128, 128),
        (0, 0, 128),
        (128, 0, 128),
        (128, 128, 64),
        (0, 64, 64),
        (0, 128, 256),
        (0, 64, 128),
        (64, 0, 255),
        (128, 64, 0),
        (255, 255, 255),
        (192, 192, 192),
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 255, 255),
        (0, 0, 255),
        (255, 0, 255),
        (255, 255, 128),
        (0, 255, 128),
        (128, 255, 255),
        (128, 128, 255),
        (255, 0, 128),
        (255, 128, 64),
    ),
             dtype=float) / 255.)

KEYMAP = (
    (cdg.Keys.LEFTARROW, '{'),
    (cdg.Keys.RIGHTARROW, '}'),
    (cdg.Keys.UPARROW, '^'),
    (cdg.Keys.DOWNARROW, 'v'),
    (cdg.Keys.FIRE, 'F'),
    (cdg.Keys.USE, 'U'),
    (cdg.Keys.ENTER, 'E'),
    (cdg.Keys.ESCAPE, 'X'),
    (None, ''),
)


class MsPaintDoom:

    def __init__(self) -> None:
        self._paint_process = subprocess.Popen(PAINT_COMMAND, shell=False)
        while (not (windows := pwc.getWindowsWithTitle(
                "Paint", condition=pwc.Re.CONTAINS))):
            pass
        time.sleep(1)
        self._window = windows[0]
        self._window.alwaysOnTop(True)
        self._window.activate(True)
        self._ticks_ms = 0
        self._last_input = None
        self._read_frame_input = True

    def _select_pencil(self) -> None:
        self._click(17, 107)

    def _select_fill_with_color(self) -> None:
        self._click(40, 57)

    def _select_color(self, idx: int) -> None:
        self._click(32 + 16 * (idx % 14), 319 + 16 * (idx // 14))

    def _select_text(self) -> None:
        self._click(40, 137)
        self._click(27, 278)

    def _select_rectangle(self) -> None:
        self._click(17, 186)

    def _click(self, x, y):
        win_x, win_y = self._window.position
        pyautogui.click(x=x + win_x, y=y + win_y)

    def _mouse_down(self, x, y):
        win_x, win_y = self._window.position
        pyautogui.mouseDown(x=x + win_x, y=y + win_y)

    def _mouse_up(self, x, y):
        win_x, win_y = self._window.position
        pyautogui.mouseUp(x=x + win_x, y=y + win_y)

    def draw_frame(self, pixels: np.ndarray) -> None:
        pixels = pixels / 255.
        pixels = filters.gaussian(pixels, channel_axis=2, sigma=2)
        pixels = np.apply_along_axis(lambda pix: np.argmin(
            color.deltaE_cie76(PALETTE_LAB, color.rgb2lab(pix[[2, 1, 0]]))),
                                     axis=2,
                                     arr=pixels)
        pixels = pixels.astype(np.uint8)
        pixels = filters.rank.modal(pixels, morphology.disk(2))
        pixels_with_border = np.pad(pixels,
                                    pad_width=1,
                                    mode='constant',
                                    constant_values=-1)

        color_idxs, color_cnts = np.unique(pixels, return_counts=True)
        color_idxs = color_idxs[np.argsort(color_cnts)[::-1]]

        # Clear screen
        with pyautogui.hold(['ctrl', 'shift']):
            pyautogui.press('n')

        # Draw framebuffer to screen
        self._select_pencil()
        for i, idx in enumerate(color_idxs):
            layer = ~np.isin(pixels, color_idxs[:i])
            layer = np.pad(layer,
                           pad_width=1,
                           mode='constant',
                           constant_values=0)
            label_layer, layer_region_cnt = measure.label(layer,
                                                          return_num=True)

            label_layer_boundaries = segmentation.find_boundaries(label_layer,
                                                                  mode="inner")
            label_layer_inner = label_layer.copy()
            label_layer_inner[label_layer_boundaries] = 0

            pyautogui.PAUSE = 0.07
            self._select_color(idx)

            for region_i in range(1, layer_region_cnt + 1):
                if not np.any((label_layer == region_i)
                              & (pixels_with_border == idx)):
                    continue
                region_contours = measure.find_contours(
                    (label_layer == region_i),
                    0.5,
                    positive_orientation='high')
                for contour in region_contours:
                    win_x, win_y = self._window.position
                    pyautogui.moveTo(61 + contour[0][1] + win_x,
                                     24 + contour[0][0] + win_y)
                    pyautogui.mouseDown()
                    pyautogui.PAUSE = 0.0006
                    for (y, x) in contour:
                        pyautogui.moveTo(61 + x + win_x, 24 + y + win_y)
                    pyautogui.PAUSE = 0.07
                    pyautogui.mouseUp()

                region_inner_segments, region_inner_segment_cnt = measure.label(
                    label_layer_inner == region_i, return_num=True)

                for region_inner_segment_i in range(
                        1, region_inner_segment_cnt + 1):
                    indices = np.argwhere(
                        region_inner_segments == region_inner_segment_i)
                    random_index = np.random.randint(0, len(indices))
                    y, x = indices[random_index]

                    self._select_fill_with_color()
                    self._click(61 + x, 24 + y)
                    self._select_pencil()

        # Draw keys
        self._select_color(0)
        for i, key in enumerate(KEYMAP):
            self._select_text()
            self._click(78 + 35 * i, 244)
            pyautogui.press(key[1])
            self._select_rectangle()
            x = 61 + 35 * i
            self._mouse_down(x, 224)
            self._mouse_up(x + 35, 264)

        self._select_fill_with_color()
        self._read_frame_input = False

    def get_key(self) -> Optional[tuple[int, int]]:
        if self._read_frame_input:
            return None
        if self._last_input is not None:
            retval = (0, self._last_input)
            self._last_input = None
            return retval
        self._read_frame_input = True
        while True:
            time.sleep(0.1)
            win_x, win_y = self._window.position
            im = np.asarray(
                pyautogui.screenshot(region=(61 + win_x, 224 + win_y, 35 * 9,
                                             40)))
            for i, key in enumerate(KEYMAP):
                x = 35 * i
                if np.all(im[0:40, x:x + 35] == 0):
                    if key[0] is None:
                        return None
                    self._last_input = key[0]
                    return (1, key[0])

    def get_ticks_ms(self) -> int:
        self._ticks_ms += 1500
        return self._ticks_ms


if __name__ == "__main__":
    g = MsPaintDoom()
    cdg.init(320, 200, g.draw_frame, g.get_key, get_ticks_ms=g.get_ticks_ms)
    cdg.main()
