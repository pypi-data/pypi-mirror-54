#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#

from __future__ import absolute_import
import os

import setuptools


def grep_version():
    path = os.path.join(os.path.dirname(__file__), 'ng_utils/__init__.py')
    with open(path) as fp:
        for line in fp:
            if line.startswith('__version__'):
                return '%s.%s.%s' % eval(' '.join(line.split()[2:]))


setuptools.setup(
    name = 'ng_utils',
    version = grep_version(),
    license = 'GPL 3',
    packages = ['ng_utils'],
    ext_package = 'ng_utils',
    ext_modules = [
        setuptools.Extension(
            name='cpython',
            sources=['ng_utils/cpython.c'],
            extra_compile_args=['-UNDEBUG', '-Wall'],
        )
    ],
    zip_safe = False,
)
