import pytest
from TeagueASM.types import hex_instruction_to_string

testdata = [
    ("4001", "JMP 1"),
    ("23FF", "IMM 1023"),
    ("FFFF", "NOOP"),
    ("FACA", "NOOP"),
    ("1005", "CP ACC 5"),
    ("3044", "ALU SUB 4"),
]


@pytest.mark.parametrize(
    (
        "test_string",
        "expected_output",
    ),
    testdata,
)
def test_parsing(
    test_string: str,
    expected_output: str,
):
    assert hex_instruction_to_string(test_string) == expected_output
