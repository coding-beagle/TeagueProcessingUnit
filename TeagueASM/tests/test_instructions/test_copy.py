import pytest
from TeagueASM.types import Copy, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("CPY 1 1", Copy(argument=[1, 1]), "1041", True, None),
    ("CPY ACC 1", Copy(argument=[0, 1]), "1001", True, None),
    ("CPY ACC PC", Copy(argument=[0, 1]), "1001", True, None),
    ("CP 52 1", Copy(argument=[52, 1]), "1D01", True, None),
    ("CP      3      55 // with comment", Copy(argument=[3, 55]), "10F7", True, None),
    ("CPY 69 737374734", Copy(argument=[69, 737374734]), "Should Fail", False, None),
    (
        "CPY 69 1 1 1 11 11 1 1 1 1 1",
        Copy(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "CP",
        Copy(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "CP saKSgjSK SKAJFKSAJKLF",
        Copy(argument=[69, 737374734]),
        "Should Fail",
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
    expected_object: Copy,
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
