"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Need to add 256 bytes of RAM
        self.ram = [0] * 255
        # 8 registers
        self.reg = [0] * 8
        # add properties for registers with PC (program counter)
        # PC and FL registers are cleared to 0
        self.pc = 0
        self.fl = 0

    def ram_read(self, mar):
        """Accept the address to read and return the value stored there"""
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        """Accept a value to write, and the address to write it to"""
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Main function 
        # Need to read memory address from register
        # Update ram_read(), ram_write()
        pass
