
"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Need to add 256 bytes of RAM
        self.ram = [0] * 256
        # 8 registers
        self.reg = [0] * 8
        # add properties for registers with PC (program counter)
        # PC (Program Counter) and FL (Flags) registers are cleared to 0
        self.pc = 0
        self.fl = 0
        # Stack Pointer
        self.sp = len(self.reg) - 1

    def ram_read(self, mar):
        """Accept the address to read and return the value stored there"""
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        """Accept a value to write, and the address to write it to"""
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.ram[mar] = mdr
    
    def load_default(self):
        """Load a program into memory."""
        print("\n==> [ Default loading ]")

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


    def load(self, file_path):
        """Load a program into memory."""
        print("\n==> Argument: [", file_path, "]")
        try:
            address = 0

            # open file to extract data
            with open(file_path) as f:
                #check each line
                for line in f:
                    comment = line.split('#')
                    num = comment[0].strip()
                    # print(comment)
                    # print(num)

                    # convert binary to string
                    data = int(num, 2) 
                    # print(data)
                    
                    # save to RAM
                    print(f'saving {data} to {address}')
                    self.ram_write(address, data)
                    address += 1
        except FileNotFoundError:
            print(f"{file_path} not found")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        # multiply
        elif op == "MUL":
            print(self.reg)
            print("reg_a", reg_a)
            print("reg_b", reg_b)
            self.reg[reg_a] *= self.reg[reg_b]
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

        LDI  = 0b10000010
        PRN  = 0b01000111
        HLT  = 0b00000001
        MUL  = 0b10100010
        PUSH = 0b01000101
        POP  = 0b01000110
        CALL = 0b01010000
        RET  = 0b00010001

        # Main function 
        # Need to read memory address from register

        # It needs to read the memory address that's stored in register PC, 
        # and store that result in IR, the Instruction Register.

        work = True

        # while - if - else cascade here
        # HLT, LDI, PRN
        print("--=== Start ===--")
        while work is True:
            self.trace()
            # IR: Instruction Register, contains a copy of the currently executing instruction
            ir = self.ram_read(self.pc)

            # Read the bytes at PC+1 and PC+2 from RAM
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                print("LDI statement", LDI )
                print('operands a', operand_a, self.ram[operand_a])
                print('operands b', operand_b, self.ram[operand_b])
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            # Multiply the values
            elif ir == MUL: 
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # Print value that is stored in the given register
            elif ir == PRN: 
                reg = operand_a
                self.reg[reg]
                print(f"PRN print {self.reg[reg]}") 
                self.pc += 2

            # halt operations
            elif ir == HLT:
                print("Halt")
                print("--===  End  ===--")
                work = False
                self.pc +=1
                sys.exit(0)
            
            elif ir == PUSH:
                # Store the value in the register into RAM at the address stored in SP

                # Grab the register argument
                reg = operand_a
                # Grab the values
                val = self.reg[reg]
                print("Push", val)                

                # Decrement the SP.
                self.reg[self.sp] -= 1

                # Copy the value in the given register to the address pointed to by SP.
                self.ram_write(self.reg[self.sp], val)
                
                # increment Program Counter
                self.pc += 2

            
            elif ir == POP:
                # Retrieve the value from RAM at the address stored in SP, and store that value in the register
                
                # Grab the register argument
                reg = operand_a
                
                # Grab the values
                val = self.ram[self.reg[self.sp]]
                self.reg[reg] = val
                print("Pop", val)                
                
                # Increment SP
                self.reg[self.sp] += 1

                # increment Program Counter
                self.pc += 2
            
            elif ir == CALL:
                pass

            elif ir == RET:
                pass
            
            else:
                print(f"Unknown command {ir}")
                sys.exit(1)
