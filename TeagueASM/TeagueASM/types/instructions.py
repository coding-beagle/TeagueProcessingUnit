from dataclasses import dataclass
from typing import Union
from .reg_aliases import REGISTER_ALIASES
from .alu_state_machine import ALU_STATE_MACHINE_NAMES


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
