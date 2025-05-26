import pytest
from TeagueASM.types import Immediate, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("IMM 1", Immediate(argument=1), "2001", True, None),
    ("IMM 2235", Immediate(argument=2235), "28BB", True, None),
    ("IMM 12 153", Immediate(argument=[12, 153]), "28BB", False, ValueError),
    ("IMM asdasdsafasgas", Immediate(argument=[12, 153]), "28BB", False, ValueError),
]


@pytest.mark.parametrize(
    (
        "test_string",
        "expected_object",
        "expected_serialisation",
        "will_succeed",
        "exception",
    ),
    testdata,
)
def test_parsing(
    test_string: str,
    expected_object: Immediate,
    expected_serialisation: str,
    will_succeed: bool,
    exception: Optional[Exception],
):
    instruction: Optional[Instruction] = None
    try:
        instruction = string_to_instruction(test_string)
        assert instruction.validate_args() == will_succeed
    except Exception as ex:
        assert type(ex) == exception  # check it raises the right exception
    if will_succeed and instruction is not None:
        assert instruction == expected_object
        assert instruction.serialise() == expected_serialisation
