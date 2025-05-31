import pytest
from TeagueASM.types import SubBranchZero, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("SUBBZ 1 1", SubBranchZero(argument=[1, 1]), "6041", True, None),
    ("SUBBZ 52 1", SubBranchZero(argument=[52, 1]), "6D01", True, None),
    (
        "SUBBZ      3      55 // with comment",
        SubBranchZero(argument=[3, 55]),
        "60F7",
        True,
        None,
    ),
    (
        "SUBBZ 69 737374734",
        SubBranchZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        None,
    ),
    (
        "SUBBZ 69 1 1 1 11 11 1 1 1 1 1",
        SubBranchZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "SUBBZ",
        SubBranchZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "SUBBZ saKSgjSK SKAJFKSAJKLF",
        SubBranchZero(argument=[69, 737374734]),
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
    expected_object: SubBranchZero,
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
