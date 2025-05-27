import pytest
from TeagueASM.parsing import initial_parse, convert_to_hex
from TeagueASM.types.instructions import *

testdata = [
    (
        [
            Copy(argument=[1, 1]),
            Immediate(argument=1023),
            Jump(argument=10),
            AluInstruction(argument=[1, 23]),
            Invert(argument=45),
        ],
        """1041
23FF
400A
3057
502D""",
    ),
]


@pytest.mark.parametrize(("test_list", "expected_hex"), testdata)
def test_parsing(
    test_list: list[Instruction],
    expected_hex: bool,
):
    assert convert_to_hex(test_list) == expected_hex
