"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    def HLT(self, a, b):
        print("HLT")
        self.running = False

    def PRN(self, a, b):
        print("PRN")
        print(self.reg[a])
        self.pc += 2

    def LDI(self, a, b):
        print("LDI")
        self.reg[a] = b
        self.pc += 3

    def MUL(self, a, b):
        print("MUL")
        self.alu("MUL", a, b)
        self.pc += 3

    def ADD(self, a, b):
        print("ADD")
        self.alu("ADD", a, b)
        self.pc += 3

    def INVALID(self, a, b):
        print(f"Instruction {self.ram_read(self.pc)} is invalid, fatal error")
        self.running = False

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        # To reduce data type bugs, we'll coerce all inputs into base-10 data
        # Starting from the dict of possible commands
        # So, the only binary handled will be on initial input, and no more

        self.commands = {
            1:   self.HLT,  # 0b00000001
            130: self.LDI,  # 0b10000010
            71:  self.PRN,  # 0b01000111
            162: self.MUL,  # 0b10100010
            160: self.ADD   # 0b10100000
        }

    # we have to define each function with multiple args, even if they don't use them all
    # this is to avoid the positional args error when conditonall executing the relevant func found in commands dict

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # # puts each item from program into ram
        # for instruction in program:
        #     self.ram[address] = bin(instruction)
        #     address += 1

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split("#")
                    number_string = comment_split[0].strip()

                    if number_string == '':
                        continue

                    num = int(number_string, 2)
                    self.ram[address] = num
                    address += 1
                    # print("{:08b} is {:d}".format(num, num))
                    print(f"{num:>08b} is {num:>0d}")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":  # TODO: Make sure this is working!!
            print("MULT received", op, reg_a, reg_b)
            print("reg_a holds ", self.reg[reg_a])
            print("reg_b holds ", self.reg[reg_b])
            self.reg[reg_a] *= self.reg[reg_b]
            print("Mul changed reg_a to", self.reg[reg_a])
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

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            print(
                f"ir: {ir} at {self.pc}, op_a: {op_a} at {self.pc+1}, op_b: {op_b} at {self.pc+2}")

            # Python doesn't have a switch statement...
            # We've defined the commands dict with references to defined functions
            # run() will iterate through ram and call the respective function based on whether it is found in the commands dict
            # This is an alternative to a switch
            # https://jaxenter.com/implement-switch-case-statement-python-138315.html
            # Check for each type of recognized command
            func = self.commands.get(ir, lambda: INVALID)
            func(op_a, op_b)

            """
            if ir is self.commands["HLT"]:
                print("HLT")
                running = False
                break
            elif ir is self.commands["PRN"]:
                print("PRN")
                output = self.reg[bin(op_a)]
                print(int(output, 2))
                self.pc += 2
            elif ir is self.commands["LDI"]:
                print("LDI")
                self.reg[int(op_a, 2)] = int(op_b, 2)
                self.pc += 3
            elif int(ir, 2) is self.commands["MUL"]:
                print("MUL")
                print("Multiply command given", op_a, op_b)
                self.alu("MUL", int(op_a, 2), int(op_b, 2))
                self.pc += 3
            elif int(ir, 2) is self.commands["ADD"]:
                print("ADD")
                self.alu("ADD", int(op_a, 2), int(op_b, 2))
                self.pc += 3
            else:
                print(
                    f"Instruction {self.ram_read(self.pc)} is invalid, fatal error")
                running = False
            """


    def ram_read(self, address):
        self.mar = address
        self.mdr = self.ram[address]
        print(f"Given {address}, ram_read returns", self.mdr)

        return self.mdr

    def ram_write(self, address, data):
        # i: value
        # i: address
        self.ram[address] = data
        self.ram_read(address)
