from dataclasses import dataclass
from typing import Union
from .reg_aliases import REGISTER_ALIASES
from .alu_state_machine import ALU_STATE_MACHINE_NAMES
from ..utils import fetch_from_dict_by_val


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
        args_joined = (self.argument[0] << 6) + self.argument[1]  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return (
            self.argument[0] < 64 and self.argument[1] < 64 and len(self.argument) == 2  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        )


@dataclass
class Immediate(Instruction):
    opcode: int = 0b0010
    required_arguments: int = 1

    def serialise(self) -> str:
        return f"{self.opcode:01X}{self.argument:03X}"

    def validate_args(self) -> bool:
        return self.argument < 4097 and isinstance(self.argument, int)  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)


@dataclass
class AluInstruction(Instruction):
    opcode: int = 0b0011
    required_arguments: int = 2

    def serialise(self) -> str:
        args_joined = (self.argument[0] << 6) + self.argument[1]  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return (
            self.argument[0] < 64 and self.argument[1] < 64 and len(self.argument) == 2  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        )


@dataclass
class Jump(Instruction):
    opcode: int = 0b0100
    required_arguments: int = 1

    def serialise(self) -> str:
        if self.argument < 0:  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
            # Convert to 12-bit two's complement
            arg_12bit = (1 << 12) + self.argument  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        else:
            arg_12bit = self.argument
        return f"{self.opcode:01X}{arg_12bit:03X}"

    def validate_args(self) -> bool:
        return -2048 <= self.argument <= 2047 and isinstance(self.argument, int)  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)


@dataclass
class Invert(Instruction):
    opcode: int = 0b0101
    required_arguments: int = 1

    def serialise(self) -> str:
        arg_to_12_bit = (0b000000 << 6) + self.argument  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        return f"{self.opcode:01X}{arg_to_12_bit:03X}"

    def validate_args(self) -> bool:
        return self.argument < 64 and isinstance(self.argument, int)  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)


@dataclass
class SubBranchZero(Instruction):
    opcode: int = 0b0110
    required_arguments: int = 2

    def serialise(self) -> str:
        args_joined = (self.argument[0] << 6) + self.argument[1]  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return (
            self.argument[0] < 64 and self.argument[1] < 64 and len(self.argument) == 2  # type: ignore -> we make sure that argument is of correct type before instantiating the class :)
        )


INSTRUCTION_STRINGS: dict[str, type[Instruction]] = {
    "NOOP": Noop,
    "CPY": Copy,
    "CP": Copy,
    "IMM": Immediate,
    "ALU": AluInstruction,
    "JMP": Jump,
    "INV": Invert,
    "SUBBZ": SubBranchZero,
}

OPCODE_STRING_DICT: dict[int, str] = {
    INSTRUCTION_STRINGS[instruction].opcode: instruction
    for instruction in INSTRUCTION_STRINGS
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

    args = [
        REGISTER_ALIASES[i] if i in REGISTER_ALIASES else i for i in args
    ]  # handle register aliases

    if command_string.strip().upper() not in INSTRUCTION_STRINGS:
        raise ValueError(
            f"ERROR ON LINE {line_num}! {command_string} is not a valid command!"
        )

    instruction_type: type[Instruction] = INSTRUCTION_STRINGS[command_string]

    if instruction_type == AluInstruction:
        if args:
            args[0] = (
                ALU_STATE_MACHINE_NAMES[args[0]]
                if args[0] in ALU_STATE_MACHINE_NAMES
                else args[0]
            )  # only replace the first arg with ALU name

    required_args: int = instruction_type.required_arguments
    if len(args) != required_args:
        raise ValueError(
            f"ERROR ON LINE {line_num}! Wrong number of args: {args}, expected {required_args}!"
        )

    if args:
        if len(args) > 1:
            try:
                return instruction_type(argument=[int(i) for i in args][:2])
            except ValueError as ex:
                raise ValueError(
                    f"ERROR ON LINE {line_num}, args {args} are not ints!"
                ) from ex
        else:
            try:
                return instruction_type(argument=int(args[0]))
            except ValueError as ex:
                raise ValueError(
                    f"ERROR ON LINE {line_num}, arg {args[0]} is not an int!"
                ) from ex
    else:
        return instruction_type()


# Should this be here or in parsing?
def hex_instruction_to_string(input_string: str, line_num: int = 0) -> str:
    """
    Given a hex string, work out what the opcode is and deduce it's args.
    Swap out the args for a named value if applicable (e.g. named registers, ALU instructions).

    Args:
        input (str): A 2 byte hex string.

    Returns:
        str: The equivalent assembly call
    """

    opcode: int = int(input_string[0], 16)
    args: int = int(input_string[1:], 16)

    output = ""

    if opcode not in OPCODE_STRING_DICT:
        raise KeyError(
            f"ERROR ON LINE {line_num}! {input_string} is not a valid instruction!"
        )

    output += OPCODE_STRING_DICT[opcode]

    arg_a: int = 0
    arg_b: int = 0

    instruction_object: type[Instruction] = INSTRUCTION_STRINGS[
        OPCODE_STRING_DICT[opcode]
    ]

    if instruction_object.required_arguments == 2:
        arg_a = (args & int(b"111111000000")) >> 6
        arg_b = args & int(b"000000111111")

        if instruction_object == AluInstruction:
            if arg_a in ALU_STATE_MACHINE_NAMES.values():
                arg_a = fetch_from_dict_by_val(ALU_STATE_MACHINE_NAMES, arg_a)
        else:
            if arg_a in REGISTER_ALIASES.values():
                arg_a = fetch_from_dict_by_val(REGISTER_ALIASES, arg_a)
            if arg_b in REGISTER_ALIASES.values():
                arg_b = fetch_from_dict_by_val(REGISTER_ALIASES, arg_b)

        output += f" {arg_a} {arg_b}"
    else:
        if instruction_object != Noop:
            output += f" {args}"

    return output
