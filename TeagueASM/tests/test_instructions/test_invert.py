import pytest
from TeagueASM.types import Invert, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("INV 1", Invert(argument=1), "5001", True, None),
    ("INV 63", Invert(argument=63), "503F", True, None),
    (
        "INV 125091251296126",
        Invert(argument=125091251296126),
        "Should fail",
        False,
        None,
    ),
    ("INV 12 153", Invert(argument=[12, 153]), "Should fail", False, ValueError),
    (
        "INV asdasdsafasgas",
        Invert(argument=[12, 153]),
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
    expected_object: Invert,
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
