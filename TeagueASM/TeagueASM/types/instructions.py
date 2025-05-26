from dataclasses import dataclass
from typing import Union


@dataclass
class Instruction:
    name: str
    opcode: int = 0b0000

    def serialise(self) -> str:
        return f"{self.opcode:01X}000"

    def validate_args(self) -> bool:
        return True


@dataclass
class Noop(Instruction):
    name: str = "NOOP"
    opcode: int = 0b1111

    def serialise(self) -> str:
        return f"{self.opcode:01X}FFF"  # DC about 12 LSBs


@dataclass
class Copy(Instruction):
    name: str = "CP"
    opcode: int = 0b0001
    args: list[int] = [0, 0]

    def serialise(self) -> str:
        args_joined = self.args[0] << 6 + self.args[1]
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return self.args[0] < 64 and self.args[1] < 64


@dataclass
class Immediate(Instruction):
    name: str = "IMM"
    opcode: int = 0b0010
    args: int = 0

    def serialise(self) -> str:
        return f"{self.opcode:01X}{self.args:03X}"

    def validate_args(self) -> bool:
        return self.args < 4097


# TODO
@dataclass
class ALU(Instruction):
    name: str = "ALU"
    opcode: int = 0b0011
    args: list[int] = [0, 0]

    def serialise(self) -> str:
        return "TODO"


# TODO
@dataclass
class Jump(Instruction):
    name: str = "JMP"
    opcode: int = 0b0100
    args: int = 0

    def serialise(self) -> str:
        return "TODO"


@dataclass
class Invert(Instruction):
    name: str = "INV"
    opcode: int = 0b0101
    args: int = 0

    def serialise(self) -> str:
        arg_to_12_bit = 0b000000 << 6 + self.args
        return f"{self.opcode:01X}{arg_to_12_bit:03X}"

    def validate_args(self) -> bool:
        return self.args < 64


@dataclass
class SubBranchNotZero(Instruction):
    name: str = "SUBBNZ"
    opcode: int = 0b0110
    args: list[int] = [0, 0]

    def serialise(self) -> str:
        args_joined = self.args[0] << 6 + self.args[1]
        return f"{self.opcode:01X}{args_joined:03X}"

    def validate_args(self) -> bool:
        return self.args[0] < 64 and self.args[1] < 64
