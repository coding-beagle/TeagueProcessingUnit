import pytest
from TeagueASM.types import Jump, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("JMP 1", Jump(argument=1), "4001", True, None),
    ("JMP 2235", Jump(argument=2235), "48BB", True, None),
    (
        "JMP 125091251296126",
        Jump(argument=125091251296126),
        "Should fail",
        False,
        None,
    ),
    ("JMP 12 153", Jump(argument=[12, 153]), "Should fail", False, ValueError),
    (
        "JMP asdasdsafasgas",
        Jump(argument=[12, 153]),
        "Should fail",
        False,
        ValueError,
    ),
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
    expected_object: Jump,
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
