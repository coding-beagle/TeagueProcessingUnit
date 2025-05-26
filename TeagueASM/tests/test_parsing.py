import pytest
from TeagueASM.parsing import parse

testdata = [
    (
        """Test 
     """,
        True,
    ),
]


@pytest.mark.parametrize(("test_code", "expected"), testdata)
def test_parsing(test_code: str, expected: bool):
    assert parse(test_code) == expected
