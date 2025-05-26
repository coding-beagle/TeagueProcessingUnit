from dataclasses import dataclass
from typing import Union, Type


@dataclass
class Instruction:
    opcode: int = 0b0000
    argument: Union[int, list[int], None] = None
    required_arguments: int = 0

    def serialise(self) -> str:
        return f"{self.opcode:01X}000"

    def validate_args(self) -> bool:
        return True


@dataclass
class Noop(Instruction):
    opcode: int = 0b1111
    required_arguments: int = 0

    def serialise(self) -> str:
        return f"{self.opcode:01X}FFF"  # DC about 12 LSBs


@dataclass
class Copy(Instruction):
    opcode: int = 0b0001
    required_arguments: int = 2

    def serialise(self) -> str:
        args_joined = (self.argument[0] << 6) + self.argument[1]
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return (
            self.argument[0] < 64 and self.argument[1] < 64 and len(self.argument) == 2
        )


@dataclass
class Immediate(Instruction):
    opcode: int = 0b0010
    required_arguments: int = 1

    def serialise(self) -> str:
        return f"{self.opcode:01X}{self.argument:03X}"

    def validate_args(self) -> bool:
        return self.argument < 4097 and isinstance(self.argument, int)


# TODO
@dataclass
class AluInstruction(Instruction):
    opcode: int = 0b0011
    required_arguments: int = 2

    def serialise(self) -> str:
        return "TODO"


# TODO
@dataclass
class Jump(Instruction):
    opcode: int = 0b0100
    required_arguments: int = 1

    def serialise(self) -> str:
        return "TODO"


@dataclass
class Invert(Instruction):
    opcode: int = 0b0101
    required_arguments: int = 1

    def serialise(self) -> str:
        arg_to_12_bit = 0b000000 << 6 + self.argument
        return f"{self.opcode:01X}{arg_to_12_bit:03X}"

    def validate_args(self) -> bool:
        return self.argument < 64 and isinstance(self.argument, int)


@dataclass
class SubBranchNotZero(Instruction):
    opcode: int = 0b0110
    required_arguments: int = 2

    def serialise(self) -> str:
        args_joined = self.argument[0] << 6 + self.argument[1]
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return (
            self.argument[0] < 64 and self.argument[1] < 64 and len(self.argument) == 2
        )


INSTRUCTION_STRINGS: dict[str, type[Instruction]] = {
    "NOOP": Noop,
    "CPY": Copy,
    "CP": Copy,
    "IMM": Immediate,
    "ALU": AluInstruction,
    "JMP": Jump,
    "INV": Invert,
    "SUBBNZ": SubBranchNotZero,
}


def string_to_instruction(input_string: str, line_num: int = 0) -> Instruction:
    """
    Take an input string and convert it to an instruction object

    Args:
        input (str): Some text

    Returns:
        Instruction object
    """
    string_without_comments: str = input_string

    if "//" in input_string:
        string_without_comments: str = input_string.split("//")[0]

    string_with_stripped_internal_whitespace: str = " ".join(
        string_without_comments.split()
    )

    split_args: list[str] = string_with_stripped_internal_whitespace.split(" ")

    command_string = split_args[0]
    args = split_args[1:]

    print(command_string)
    print(command_string.strip().upper() not in INSTRUCTION_STRINGS)

    if command_string.strip().upper() not in INSTRUCTION_STRINGS:
        raise ValueError(
            f"ERROR ON LINE {line_num}! {command_string} is not a valid command!"
        )

    instruction_type: type[Instruction] = INSTRUCTION_STRINGS[command_string]

    if args and len(args) == instruction_type.required_arguments:
        if len(args) > 1:
            return instruction_type(argument=[int(i) for i in args][:2])
        else:
            return instruction_type(argument=int(args[0]))
    else:
        return instruction_type()
