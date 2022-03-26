from asyncio.windows_events import NULL
from copy import deepcopy


def main():
    int_code_runner = IntCodeRunner(
        path="./day5Input.txt",
        parameter_reader=read_parameter,
        ops={
            1: add,
            2: mul,
            3: save,
            4: out,
            5: jmpt,
            6: jmpf,
            7: lt,
            8: eq,
        },
        default_op=invalid_op,
    )
    int_code_runner.run_int_code()


class IntCodeRunner():
    def __init__(self, **kwargs):
        if "path" in kwargs:
            self.int_code = self.read_int_code(kwargs["path"])
        self.parameter_reader = kwargs["parameter_reader"] if "parameter_reader" in kwargs else lambda **kwargs: kwargs["int_code"][kwargs["int_code"][kwargs["parameter_pointer"]]]
        self.ops = kwargs["ops"] if "ops" in kwargs else {}
        self.halt_code = kwargs["halt_code"] if "halt_code" in kwargs else 99
        self.default_op = kwargs["default_op"] if "default_op" in kwargs else lambda **kwargs: kwargs["instruction_pointer"]

    def read_int_code(self, path):
        int_code = []
        with open(path) as f:
            int_code = f.readlines()[0].split(",")

        return [int(num) for num in int_code]

    def read_instruction(self, instruction):
        instruction = str(instruction).rjust(5, '0')
        op_code = int(instruction[3:])
        parameter_modes = [int(parameter_mode)
                           for parameter_mode
                           in instruction[0:3]]
        parameter_modes.reverse()
        return op_code, parameter_modes

    def run_int_code(self):
        int_code = deepcopy(self.int_code)

        instruction_pointer = 0
        while True:
            op_code, parameter_modes = self.read_instruction(
                int_code[instruction_pointer])

            if op_code == self.halt_code:
                return int_code[0]
            elif op_code in self.ops:
                instruction_pointer = self.ops[op_code](
                    int_code=int_code,
                    instruction_pointer=instruction_pointer,
                    parameter_reader=self.parameter_reader,
                    parameter_modes=parameter_modes,
                )
            else:
                instruction_pointer = self.default_op(
                    int_code=int_code,
                    instruction_pointer=instruction_pointer,
                    parameter_reader=self.parameter_reader,
                    parameter_modes=parameter_modes,
                )


def invalid_op(**kwargs):
    print(
        f"Invalid command: {kwargs['op_code']} at: {kwargs['instruction_pointer']}")
    return kwargs["instruction_pointer"]


def read_parameter(**kwargs):
    parameter_number = kwargs["parameter_number"] if "parameter_number" in kwargs else 1
    if kwargs["parameter_mode"] == 0:
        return kwargs["int_code"][kwargs["int_code"][kwargs["instruction_pointer"] + parameter_number]]
    if kwargs["parameter_mode"] == 1:
        return kwargs["int_code"][kwargs["instruction_pointer"] + parameter_number]


def add(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    save_location = kwargs["parameter_reader"](
        parameter_number=3,
        parameter_mode=1,
        **kwargs
    )
    kwargs["int_code"][save_location] = first_parameter + second_parameter
    return kwargs["instruction_pointer"] + 4


def mul(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    save_location = kwargs["parameter_reader"](
        parameter_number=3, parameter_mode=1, **kwargs)
    kwargs["int_code"][save_location] = first_parameter * second_parameter
    return kwargs["instruction_pointer"] + 4


def save(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=1,
        **kwargs
    )
    kwargs["int_code"][first_parameter] = int(
        input(f"Please input in integer to store at location {first_parameter}: "))
    return kwargs["instruction_pointer"] + 2


def out(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    print(first_parameter)
    return kwargs["instruction_pointer"] + 2


def jmpt(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    if first_parameter != 0:
        return second_parameter
    return kwargs["instruction_pointer"] + 3


def jmpf(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    if first_parameter == 0:
        return second_parameter
    return kwargs["instruction_pointer"] + 3


def lt(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    save_location = kwargs["parameter_reader"](
        parameter_number=3,
        parameter_mode=1,
        **kwargs
    )
    if first_parameter < second_parameter:
        kwargs["int_code"][save_location] = 1
    else:
        kwargs["int_code"][save_location] = 0
    return kwargs["instruction_pointer"] + 4


def eq(**kwargs):
    first_parameter = kwargs["parameter_reader"](
        parameter_number=1,
        parameter_mode=kwargs["parameter_modes"][0],
        **kwargs
    )
    second_parameter = kwargs["parameter_reader"](
        parameter_number=2,
        parameter_mode=kwargs["parameter_modes"][1],
        **kwargs
    )
    save_location = kwargs["parameter_reader"](
        parameter_number=3, parameter_mode=1, **kwargs)
    if first_parameter == second_parameter:
        kwargs["int_code"][save_location] = 1
    else:
        kwargs["int_code"][save_location] = 0
    return kwargs["instruction_pointer"] + 4


if __name__ == "__main__":
    main()
