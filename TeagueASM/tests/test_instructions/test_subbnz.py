import pytest
from TeagueASM.types import SubBranchNotZero, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("SUBBNZ 1 1", SubBranchNotZero(argument=[1, 1]), "6041", True, None),
    ("SUBBNZ 52 1", SubBranchNotZero(argument=[52, 1]), "6D01", True, None),
    (
        "SUBBNZ      3      55 // with comment",
        SubBranchNotZero(argument=[3, 55]),
        "60F7",
        True,
        None,
    ),
    (
        "SUBBNZ 69 737374734",
        SubBranchNotZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        None,
    ),
    (
        "SUBBNZ 69 1 1 1 11 11 1 1 1 1 1",
        SubBranchNotZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "SUBBNZ",
        SubBranchNotZero(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "SUBBNZ saKSgjSK SKAJFKSAJKLF",
        SubBranchNotZero(argument=[69, 737374734]),
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
    expected_object: SubBranchNotZero,
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
