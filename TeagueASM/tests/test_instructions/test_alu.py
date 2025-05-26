import pytest
from TeagueASM.types import AluInstruction, string_to_instruction, Instruction
from typing import Optional

testdata = [
    ("ALU 1 1", AluInstruction(argument=[1, 1]), "3041", True, None),
    ("ALU ADD 1", AluInstruction(argument=[0, 1]), "3001", True, None),
    ("ALU SUB PC", AluInstruction(argument=[1, 1]), "3041", True, None),
    ("ALU 52 1", AluInstruction(argument=[52, 1]), "3D01", True, None),
    (
        "ALU      3      55 // with comment",
        AluInstruction(argument=[3, 55]),
        "30F7",
        True,
        None,
    ),
    (
        "ALU 69 737374734",
        AluInstruction(argument=[69, 737374734]),
        "Should Fail",
        False,
        None,
    ),
    (
        "ALU 69 1 1 1 11 11 1 1 1 1 1",
        AluInstruction(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "ALU",
        AluInstruction(argument=[69, 737374734]),
        "Should Fail",
        False,
        ValueError,
    ),
    (
        "ALU saKSgjSK SKAJFKSAJKLF",
        AluInstruction(argument=[69, 737374734]),
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
    expected_object: AluInstruction,
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
