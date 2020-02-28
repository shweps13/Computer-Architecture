
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
        self.fl = [0] * 8
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
                    # print("Num", num)
                    if num == '':
                        continue

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
        elif op == "CMP":
            # last 3 digits in self.fl => [00000LGE] are showing us [E]qual, [L]ower or [G]reater  mark
            # if reg_a = reg_b => set [E] flag to 1, otherwise 0
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl[7] = 1
                print("[  Equal  ]")
            # if reg_a < reg_b => set [L] flag to 1, otherwise 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[5] = 1
                print("[  Lower  ]")
            # if reg_a > reg_b => set [G] flag to 1, otherwise 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl[6] = 6
                print("[  Greater  ]")
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
        ADD  = 0b10100000
        PUSH = 0b01000101
        POP  = 0b01000110
        CALL = 0b01010000
        RET  = 0b00010001
        CMP  = 0b10100111
        JMP  = 0b01010100
        JEQ  = 0b01010101
        JNE  = 0b01010110

        # Main function 
        # Need to read memory address from register

        # It needs to read the memory address that's stored in register PC, 
        # and store that result in IR, the Instruction Register.

        work = True

        # while - if - else cascade here
        # HLT, LDI, PRN
        print("--=== Start ===--")
        while work is True:
            # self.trace()
            # IR: Instruction Register, contains a copy of the currently executing instruction
            ir = self.ram_read(self.pc)

            # Read the bytes at PC+1 and PC+2 from RAM
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                # print("LDI statement", LDI )
                print('operands a', operand_a, self.ram[operand_a])
                print('operands b', operand_b, self.ram[operand_b])
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            # Multiply the values
            elif ir == MUL: 
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            # Print value that is stored in the given register
            elif ir == PRN: 
                reg = operand_a
                self.reg[reg]
                print("================") 
                print(f"PRN print {self.reg[reg]}") 
                print("================") 
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
                # Decrement the Stack Pointer
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
                # Increment Stack Pointer
                self.reg[self.sp] += 1
                # increment Program Counter
                self.pc += 2
            
            elif ir == CALL:
                # The address of the instruction directly after CALL is pushed onto the stack.
                val = self.pc + 2
                # PC is set to the address stored in the given register
                reg_index = operand_a 
                subroutine_address = self.reg[reg_index]
                # Decrement the Stack Pointer
                self.reg[self.sp] -= 1
                # PC is set to the address stored in the given register
                self.ram[self.reg[self.sp]] = val
                reg = operand_a
                subroutine_address = self.reg[reg]
                print("reg: ", reg)
                self.pc = subroutine_address

            elif ir == RET:
                # return for the subroutine
                return_address = self.reg[self.sp]
                # pop value from stack
                self.pc = self.ram_read(return_address)
                # Increment Stack Pointer
                self.reg[self.sp] += 1
            
            elif ir == CMP:
                # Compare 2 values
                self.alu("CMP", operand_a, operand_b)
                print("^ Compare ^")
                # print("Register: ", self.reg)
                # print("Flag: ", self.reg[self.fl])
                self.pc += 3

            elif ir == JMP:
                # Jump to the address stored in the given register.
                # Set the PC to the address stored in the given register.
                self.pc = self.reg[operand_a]
                print("Jump address: ", self.pc)
                # print("Program Counter ", self.pc)

            elif ir == JEQ:
                # If equal flag is set (true), jump to the address stored in the given register.
                if self.fl[7] == 1:
                    self.pc = self.reg[operand_a]
                    print("Jump to: ", self.pc)
                else:
                    print("JEQ command, but skipped")
                    self.pc += 2

            elif ir == JNE:
                # If E flag is clear (false, 0), jump to the address stored in the given register.
                if self.fl[7] == 0:
                    self.pc = self.reg[operand_a]
                    print("Jump to: ", self.pc)
                else:
                    print("JNE command, but skipped")
                    self.pc += 2

            else:
                print(f"Unknown command {ir}")
                sys.exit(1)
