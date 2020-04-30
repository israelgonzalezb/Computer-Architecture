import sys

PRINT_TIM = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4
PRINT_REGISTER = 5

memory = [
    PRINT_TIM,
    PRINT_TIM,
    PRINT_TIM,
    PRINT_NUM,
    14,
    SAVE,
    101,
    1,
    PRINT_REGISTER,
    0,
    HALT
]

# registers are tiny bits of coded that are written on the cpu
# these are very fast
# they are always referred to as R0, R1, etc

running = True
pc = 0

# [0,0,0,0,0,0,0,0]
registers = [0] * 8

while running is True:
    command = memory[pc]

    if command == PRINT_TIM:
        print("Tim!")
        pc += 1

    if command == PRINT_NUM:
        print(memory[pc + 1])
        pc += 2

    if command == SAVE:
        registers[memory[pc + 2]] = memory[pc + 1]
        pc += 3

    if command == HALT:
        running = False

    else:
        print("Error!")
        sys.exit(1)
