import pytest
from TeagueASM.types import Copy, string_to_instruction, Instruction

testdata = [
    ("CP 1 1", Copy(argument=[1, 1]), "1041", True),
    ("CP 52 1", Copy(argument=[52, 1]), "1D01", True),
    ("CP      3      55 // with comment", Copy(argument=[3, 55]), "10F7", True),
    ("CP 69 737374734", Copy(argument=[52, 1]), "Should Fail", False),
]


@pytest.mark.parametrize(
    ("test_string", "expected_object", "expected_serialisation", "will_succeed"),
    testdata,
)
def test_parsing(
    test_string: str,
    expected_object: Copy,
    expected_serialisation: str,
    will_succeed: bool,
):
    instruction: Instruction = string_to_instruction(test_string)
    assert instruction.validate_args() == will_succeed
    assert instruction == expected_object
    assert instruction.serialise() == expected_serialisation
