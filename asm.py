from __future__ import print_function
from cpu import CPU

source = open("test.asm")
debug = False
instructions = [line.strip().replace("\n", "").split(" ") for line in source if line and line.strip()]

try:
    cpu = CPU(instructions)
    while not cpu.finished():
        cpu.process()
except Exception as e:
    print(e)
