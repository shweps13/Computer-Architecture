#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# print(sys.argv)

cpu = CPU()

if len(sys.argv) == 1:
    cpu.load_default()
elif len(sys.argv) == 2:
    cpu.load(sys.argv[1])

cpu.run()