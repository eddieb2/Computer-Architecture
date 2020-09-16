"""CPU functionality."""

import sys

# Instructions
HLT = 0b00000001 # 1
LDI = 0b10000010 # 130
PRN = 0b01000111 # 71
MUL = 0b10100010 # 162

class CPU:
    """Main CPU class."""

    def __init__(self):
        # Memory
        self.ram = [0] * 256
        # Registers -> variables in hardware - fixed num and name of these registers
        self.reg = [0] * 8
        # Program Counter -> Address of the currently executing instruction
        self.pc = 0
        # Keeps us running or stopped
        self.running = True

    '''
    `MAR`: Memory Address Register
    =>> holds the memory address we're reading or writing
    
    `MDR`: Memory Data Register
    =>> holds the value to write or the value just read
    '''
    ## RAM read ##
    def ram_read(self, MAR):
        return self.ram[MAR]

    ## RAM write ##
    def ram_write(self, MAR, MDR):
        # ram location = value
        self.ram[MAR] = MDR

    # ORIGINAL LOAD
    # def load(self):
    #     """Load a program into memory."""
    #
    #     address = 0
    #
    #     # For now, we've just hardcoded a program:
    #
    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000, # 0
    #         0b00001000, # 8
    #         0b01000111, # PRN R0
    #         0b00000000, # 0
    #         0b00000001, # HLT
    #     ]
    #
    #     # Saves each instruction to a new address in memory
    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    # NEW LOAD
    def load(self):
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    # base 2
                    try:
                        value = int(n, 2)
                    except ValueError:
                        print(f'Invalid number {value}')
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print('File not found.')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
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
        while self.running is True:
            # Instruction Register -> copy of currently executing instructions
            # ram @ index 0 to start .. LDI 130
            ir = self.ram[self.pc]

            op_1 = self.ram_read(self.pc + 1)
            op_2 = self.ram_read(self.pc + 2)

            # print(f'{op_1, op_2}')

            if ir == HLT:
                # print(f'HLT: {ir}')
                self.running = False
                self.pc += 1
                # print(self.pc)
            elif ir == LDI:
                # print(f'LDI: {ir}')
                # Store op_2 in a register at index op_1 or 0
                self.reg[op_1] = op_2
                self.pc += 3
                # print(self.pc)
            elif ir == PRN:
                # print(f'PRN: {ir}')
                # Print value stored at reg[0] which is 8
                print(self.reg[op_1])
                # Increment PC to halt
                self.pc += 2
                # print(self.pc)
            elif ir == MUL:
                self.alu('MUL', op_1, op_2)
                self.pc += 3
            else:
                print("Broken")
        # print(self.ram)

c1 = CPU()
# c1.load()
