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


from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize
import numpy


setup(
    name="cydoomgeneric",
    description="Easily portable doom for python",
    version="0.1.0",
    author="Wojciech Graj",
    url="https://github.com/wojciech-graj/cydoomgeneric",
    license="GPL-2.0-or-later",
    ext_modules=cythonize(
        [
            Extension(
                "cydoomgeneric",
                sources=["cydoomgeneric.pyx"],
                include_dirs=["./../doomgeneric", numpy.get_include()],
                define_macros=[
                    ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
                ],
                libraries=["doomgeneric"],
                extra_objects=["./../doomgeneric/libdoomgeneric.so"],
                extra_link_args=["-L./../doomgeneric"]
            )
        ],
        language_level=2
    ),
    install_requires=['numpy>=1.20'],
)
