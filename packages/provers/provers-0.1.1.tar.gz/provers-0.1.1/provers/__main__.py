#!/usr/bin/env python3
# Copyright (C) 2019, Miklos Maroti
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import subprocess
import sys

from . import __version__


def run():
    print("python version:", sys.version.replace('\n', ' '))
    print("provers version:", __version__)

    p = subprocess.Popen(['prover9'], stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    m = re.match(r'^(?:[^\n]*\n)*(Prover[^\n]*)\n',
                 p.communicate()[0].decode('ascii'))
    print("prover9 version", m.group(1) if m else 'not found')

    p = subprocess.Popen(['mace4'], stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    m = re.match(r'^(?:[^\n]*\n)*(Mace[^\n]*)\n',
                 p.communicate()[0].decode('ascii'))
    print("mace4 version:", m.group(1) if m else 'not found')


if __name__ == '__main__':
    run()
