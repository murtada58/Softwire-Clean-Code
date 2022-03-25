from copy import deepcopy

def main():
    int_code = read_int_code("./day2Input.txt")
    # print(run_int_code(int_code))

    for i in range(0, 99):
        for j in range(0, 99):
            int_code_copy = deepcopy(int_code)
            int_code_copy[1] = i
            int_code_copy[2] = j
            if 19690720 == run_int_code(int_code_copy):
                print((i * 100) + j)
                return


def read_int_code(path):
    int_code = []
    with open(path) as f:
        int_code = f.readlines()[0].split(",")

    return [int(num) for num in int_code]

def run_int_code(int_code):
    for i in range(0, len(int_code), 4):
        operation_code = int_code[i]

        if operation_code == 99:
            return int_code[0]

        first_operand_location = int_code[i + 1]
        second_operand_location = int_code[i + 2]
        save_location = int_code[i + 3]

        if operation_code == 1:
            int_code[save_location] = int_code[first_operand_location] + int_code[second_operand_location]

        elif operation_code == 2:
            int_code[save_location] = int_code[first_operand_location] * int_code[second_operand_location]

if __name__ == "__main__":
    main()