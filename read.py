import sys

# try:
#     file = open("print8.ls8", 'r')
#     lines = file.read()
#     print(lines)

#     raise Exception("hi")
# except Exception:
#     print(file.closed)


# try:
#     with open("print8.ls8") as file:
#         for line in file:
#             print(line)
#             raise Exception("hi")
# except Exception:
#     print(file.closed)

# if len(sys.argv) != 2:
#     print(f"usage: {sys.argv[0]} filename")
#     sys.exit(2)

try:
    with open(sys.argv[1]) as file:
        for line in file:
            comment_split = line.split("#")
            number_string = comment_split[0].strip()

            if number_string == '':
                continue

            num = int(number_string, 2)
            # print("{:08b} is {:d}".format(num, num))
            print(f"{num:>08b} is {num:>0d}")


except FileNotFoundError:
    print(f"{sys.argv[0]}: could not find {sys.argv[1]}")
    sys.exit(2)
