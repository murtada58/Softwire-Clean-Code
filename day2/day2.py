
import opcode


program = []
with open("./day2Input.txt") as f:
    program = f.readlines()[0].split(",")

program = [int(num) for num in program]

for i in range(0, len(program), 4):
    operation_code = program[i]
    if operation_code == 99:
        print(program[0])
        break
    first_operand_location = program[i + 1]
    second_operand_location = program[i + 2]
    save_location = program[i + 3]

    if operation_code == 1:
        program[save_location] = program[first_operand_location] + program[second_operand_location]

    elif operation_code == 2:
        program[save_location] = program[first_operand_location] * program[second_operand_location]