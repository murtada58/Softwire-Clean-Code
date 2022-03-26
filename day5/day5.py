from copy import deepcopy

def main():
    int_code_runner = IntCodeRunner("./day5Input.txt")
    int_code_runner.run_int_code()
    

class IntCodeRunner():
    def __init__(self, path):
        self.int_code = self.read_int_code(path)

    def read_int_code(self, path):
        int_code = []
        with open(path) as f:
            int_code = f.readlines()[0].split(",")

        return [int(num) for num in int_code]

    def read_instruction(self, instruction):
        instruction = str(instruction).rjust(5, '0')
        op_code = int(instruction[3:])
        parameter_modes = [int(parameter_mode) for parameter_mode in instruction[0:3]]
        parameter_modes.reverse()
        return op_code, parameter_modes

    def run_int_code(self):
        int_code = deepcopy(self.int_code)

        instruction_pointer = 0
        while True:
            op_code, parameter_modes = self.read_instruction(int_code[instruction_pointer])
            # print(instruction_pointer, op_code)
            if op_code == 99:
                return int_code[0]
            elif op_code == 1:
                instruction_pointer = self.add(int_code, instruction_pointer, parameter_modes)
            elif op_code == 2:
                instruction_pointer = self.mul(int_code, instruction_pointer, parameter_modes)
            elif op_code == 3:
                instruction_pointer = self.save(int_code, instruction_pointer)
            elif op_code == 4:
                instruction_pointer = self.out(int_code, instruction_pointer, parameter_modes)
            elif op_code == 5:
                instruction_pointer = self.jmpt(int_code, instruction_pointer, parameter_modes)
            elif op_code == 6:
                instruction_pointer = self.jmpf(int_code, instruction_pointer, parameter_modes)
            elif op_code == 7:
                instruction_pointer = self.lt(int_code, instruction_pointer, parameter_modes)
            elif op_code == 8:
                instruction_pointer = self.eq(int_code, instruction_pointer, parameter_modes)
            else:
                print(f"Invalid command: {op_code} at: {instruction_pointer}")
                return -1
        


    def read_parameter(self, int_code, parameter_pointer, parameter_mode):
        if parameter_mode == 0:
            return int_code[int_code[parameter_pointer]]
        if parameter_mode == 1:
            return int_code[parameter_pointer]

    def add(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        save_location = self.read_parameter(int_code, instruction_pointer + 3, 1)
        int_code[save_location] = first_parameter + second_parameter
        return instruction_pointer + 4

    def mul(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        save_location = self.read_parameter(int_code, instruction_pointer + 3, 1)
        int_code[save_location] = first_parameter * second_parameter
        return instruction_pointer + 4

    def save(self, int_code, instruction_pointer):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, 1)
        int_code[first_parameter] = int(input(f"Please input in integer to store at location {first_parameter}: "))
        return instruction_pointer + 2
    
    def out(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        print(first_parameter)
        return instruction_pointer + 2

    def jmpt(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        if first_parameter != 0: return second_parameter
        return instruction_pointer + 3

    def jmpf(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        if first_parameter == 0: return second_parameter
        return instruction_pointer + 3

    def lt(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        save_location = self.read_parameter(int_code, instruction_pointer + 3, 1)
        if first_parameter < second_parameter: int_code[save_location] = 1
        else: int_code[save_location] = 0
        return instruction_pointer + 4

    def eq(self, int_code, instruction_pointer, parameter_modes):
        first_parameter = self.read_parameter(int_code, instruction_pointer + 1, parameter_modes[0])
        second_parameter = self.read_parameter(int_code, instruction_pointer + 2, parameter_modes[1])
        save_location = self.read_parameter(int_code, instruction_pointer + 3, 1)
        if first_parameter == second_parameter: int_code[save_location] = 1
        else: int_code[save_location] = 0
        return instruction_pointer + 4

if __name__ == "__main__":
    main()