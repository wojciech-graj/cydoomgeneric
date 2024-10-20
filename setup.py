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


from setuptools import Extension, setup
from Cython.Build import cythonize
import Cython
import numpy
import sys


doom_src = (
    "am_map.c",
    "d_event.c",
    "d_items.c",
    "d_iwad.c",
    "d_loop.c",
    "d_main.c",
    "d_mode.c",
    "d_net.c",
    "doomdef.c",
    "doomgeneric.c",
    "doomstat.c",
    "dstrings.c",
    "dummy.c",
    "f_finale.c",
    "f_wipe.c",
    "g_game.c",
    "hu_lib.c",
    "hu_stuff.c",
    "i_cdmus.c",
    "i_endoom.c",
    "i_input.c",
    "i_joystick.c",
    "i_scale.c",
    "i_sound.c",
    "i_system.c",
    "i_timer.c",
    "i_video.c",
    "info.c",
    "m_argv.c",
    "m_bbox.c",
    "m_cheat.c",
    "m_config.c",
    "m_controls.c",
    "m_fixed.c",
    "m_menu.c",
    "m_misc.c",
    "m_random.c",
    "memio.c",
    "p_ceilng.c",
    "p_doors.c",
    "p_enemy.c",
    "p_floor.c",
    "p_inter.c",
    "p_lights.c",
    "p_map.c",
    "p_maputl.c",
    "p_mobj.c",
    "p_plats.c",
    "p_pspr.c",
    "p_saveg.c",
    "p_setup.c",
    "p_sight.c",
    "p_spec.c",
    "p_switch.c",
    "p_telept.c",
    "p_tick.c",
    "p_user.c",
    "r_bsp.c",
    "r_data.c",
    "r_draw.c",
    "r_main.c",
    "r_plane.c",
    "r_segs.c",
    "r_sky.c",
    "r_things.c",
    "s_sound.c",
    "sha1.c",
    "sounds.c",
    "st_lib.c",
    "st_stuff.c",
    "statdump.c",
    "tables.c",
    "v_video.c",
    "w_checksum.c",
    "w_file.c",
    "w_file_stdc.c",
    "w_main.c",
    "w_wad.c",
    "wi_stuff.c",
    "z_zone.c",
)


libraries = []
define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
extra_compile_args = []
extra_link_args = []
compiler_directives = {}


if sys.platform == "win32":
    libraries.append("user32")
else:
    define_macros.extend([
        ("NORMALUNIX", None),
        ("LINUX", None),
        ("_DEFAULT_SOURCE", None)
    ])
    extra_compile_args.append("-Os")


setup(
    url="https://github.com/wojciech-graj/cydoomgeneric",
    ext_modules=cythonize(
        [
            Extension(
                "cydoomgeneric",
                sources=[
                    "./cydoomgeneric/cydoomgeneric.pyx"
                ]
                + [f"./doomgeneric/{src}" for src in doom_src],
                include_dirs=[
                    "./doomgeneric",
                    numpy.get_include()
                ],
                define_macros=define_macros,
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args,
                libraries=libraries
            )
        ],
        language_level=3,
        compiler_directives=compiler_directives
    ),
)
