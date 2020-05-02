"""CPU functionality."""

import sys

dev = False

def printDev(text1="", text2="", text3=""):
    if dev == True:
        print(text1, text2, text3)

class CPU:
    """Main CPU class."""
    def HLT(self, a, b):
        printDev("HLT")
        self.running = False

    def PRN(self, a, b):
        printDev("PRN")
        print(self.reg[a])
        self.pc += 2

    def LDI(self, a, b):
        printDev("LDI")
        self.reg[a] = b
        self.pc += 3

    def MUL(self, a, b):
        printDev("MUL")
        self.alu("MUL", a, b)
        self.pc += 3

    def ADD(self, a, b):
        printDev("ADD")
        self.alu("ADD", a, b)
        self.pc += 3
    
    def CMP(self, a, b):
        printDev("CMP")
        self.alu("CMP", a, b)
        self.pc += 3

    def PUSH(self, a, b):
        printDev("PUSH")
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp],self.reg[a])
        self.pc += 2

    def POP(self, a, b):
        printDev("POP")
        data = self.ram_read(self.reg[self.sp])
        self.reg[a] = data
        self.reg[self.sp] += 1
        self.pc += 2

    def CALL(self, a, b):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc + 2)

        self.pc = self.reg[a]

    def RET(self, a, b):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def PRA(self, a, b):
        printDev("PRA")
        print(chr(b))
        self.pc += 2

    def JMP(self, a, b):
        printDev("JMP")
        self.pc = self.reg[a]

    def JEQ(self, a, b):
        printDev("JEQ")
        # Use AND mask to check whether E flag is true
        if (self.reg[self.fl] & 0b1) == 1:
            # self.JMP(a, b)
            self.pc = self.reg[a]
        else:
            self.pc += 2

    def JNE(self, a, b):
        printDev("JNE")
        # Use OR mask to check whether E flag is false
        if (self.reg[self.fl] & 0b1111110) == self.reg[self.fl]:
            printDev(f"E flag is false {bin(self.reg[self.fl])}")
            printDev(f"Given address {a} which is {self.reg[a]}")
            printDev(f"The command at {self.reg[a]} is {self.ram[self.reg[a]]}")
            # self.JMP(a, b)
            self.pc = self.reg[a]
        else:
            self.pc += 2

    def INVALID(self, a, b):
        print(f"Instruction {self.ram_read(self.pc)} is invalid, fatal error")
        self.running = False

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        # R7 (self.reg[self.sp]) is reserved as the stack pointer (SP)
        self.sp = 7 
        # R4 will be used as flags register
        self.fl = 4 
        # FL bits: 00000LGE
        self.reg[self.fl] = 0b00000000 

        # To reduce data type bugs, we'll coerce all inputs into base-10 data
        # Starting from the dict of possible commands
        # So, the only binary handled will be on initial input, and no more
        self.commands = {
            1:   self.HLT,  # 0b00000001
            130: self.LDI,  # 0b10000010
            71:  self.PRN,  # 0b01000111
            162: self.MUL,  # 0b10100010
            160: self.ADD,  # 0b10100000
            69: self.PUSH,  # 0b01000101 
            70: self.POP,   # 0b01000110
            80: self.CALL,  # 0b0101000
            17: self.RET,   # 0b0010001
            72: self.PRA,   # 0b01001000
            167: self.CMP,  # 0b10100111
            84: self.JMP,   # 0b01010100
            85: self.JEQ,   # 0b01010101
            86: self.JNE    # 0b01010110
        }

    # we have to define each function with multiple args, even if they don't use them all
    # this is to avoid the positional args error when conditonally executing the relevant func found in commands dict

    def load(self):
        address = 0

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split("#")
                    number_string = comment_split[0].strip()

                    if number_string == '':
                        continue

                    num = int(number_string, 2) # coerce input data from binary to base-10
                    self.ram[address] = num
                    address += 1
                    # print("{:08b} is {:d}".format(num, num))
                    printDev(f"{num:>08b} is {num:>0d}")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            printDev("MULT received", op, reg_a, reg_b)
            printDev("reg_a holds ", self.reg[reg_a])
            printDev("reg_b holds ", self.reg[reg_b])
            self.reg[reg_a] *= self.reg[reg_b]
            printDev("Mul changed reg_a to", self.reg[reg_a])
        elif op == "CMP":
            # Compare reg_a and reg_b
            # FL bits: 00000LGE
            printDev(f"Comparing {self.reg[reg_a]} and {self.reg[reg_b]}")
            if self.reg[reg_a] == self.reg[reg_b]:
                # If they are equal, set E flag to 1, otherwise set it to 0
                self.reg[self.fl] = self.reg[self.fl] | 0b1
            else:
                self.reg[self.fl] = self.reg[self.fl] & 0b11111110

            # if reg_a is less than reg_b, set L flag to 1, otherwise 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.reg[self.fl] = self.reg[self.fl] | 0b100
            else:
                self.reg[self.fl] = self.reg[self.fl] & 0b11111011

            # if reg_a is greater than reg_b, set G flag to 1, otherwise 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.reg[self.fl] = self.reg[self.fl] | 0b10
            else:
                self.reg[self.fl] = self.reg[self.fl] & 0b11111011
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """Run the CPU."""
        self.running = True # We could replace this with sys.exit(0)
        #self.timer = time.perf_counter() # import time
        while self.running:
            ir = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            #print(
            #    f"ir: {ir} at {self.pc}, op_a: {op_a} at {self.pc+1}, op_b: {op_b} at {self.pc+2}")

            # if time.perf_counter() - self.timer >= 1:
            #     self.timer = time.perf_counter()
            #     self.reg[6] = 0b1 # Fix this.... 

            #     maskedInterrupts = self.reg[5] & self.reg[6] # bitwise mask operation

            #     interrupts_string = f"{maskedInterrupts:>08b}"

            #     for i in range(0, 8):
            #         is_bit_set = interrupts_string[i] == "1"
            #         self.interrupts_allowed = False
            #         self.reg[6] = 0 # we want to set a specific bit off, not all like how this is currently written
            #         # TODO: Push pc reg to stack
            #         # TODO: Push FL to stack
            #         # TODO: Push R0-R6 to stack in order

                # TODO: implement IRET


            # Python doesn't have a switch statement...
            # We've defined the commands dict with references to defined functions
            # run() will iterate through ram and call the respective function based on whether it is found in the commands dict
            # This is an alternative to a switch
            # https://jaxenter.com/implement-switch-case-statement-python-138315.html
            # Check for each type of recognized command
            func = self.commands.get(ir, self.INVALID)
            func(op_a, op_b)


    def ram_read(self, address):
        self.mar = address
        self.mdr = self.ram[address]
        printDev(f"Given {address}, ram_read returns", self.mdr)

        return self.mdr

    def ram_write(self, address, data):
        # i: value
        # i: address
        self.ram[address] = data
        self.ram_read(address)
