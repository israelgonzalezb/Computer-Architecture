"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.commands = {
            "HLT": 0b00000001,
            "LDI": 0b10000010,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "ADD": 0b10100000 
        }

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
                    self.ram[address] = bin(num)
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
        elif op == "MUL":
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
        running = True
        while running:
            command = self.ram[self.pc]
            # Python doesn't have a switch statement...
            # Check for each type of recognized command
            ir = self.ram_read(self.pc)

            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]
            if int(command, 2) is self.commands["HLT"]:
                running = False
                break
            elif int(command, 2) is self.commands["PRN"]:
                output = self.ram_read(int(op_a, 2))
                print(int(output,2))
                self.pc += 2
            elif int(command, 2) is self.commands["LDI"]:
                self.ram_write(int(op_a, 2), op_b)
                self.pc += 3
            elif int(command, 2) is self.commands["MUL"]:
                self.alu("MUL",int(op_a,2),int(op_b,2))
                self.pc += 3
            elif int(command, 2) is self.commands["ADD"]:
                self.alu("ADD",int(op_a,2),int(op_b,2))
                self.pc += 3
            else:
                print(
                    f"Instruction {self.ram_read(self.pc)} is invalid, fatal error")
                running = False

    def ram_read(self, address):
        self.mar = address
        self.mdr = self.ram[address]

        return self.mdr

    def ram_write(self, address, data):
        # i: value
        # i: address
        self.ram[address] = data
        self.ram_read(address)


