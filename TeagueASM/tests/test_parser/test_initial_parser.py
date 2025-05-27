import pytest
from TeagueASM.parsing import initial_parse

testdata = [
    (
        """CP 00 00
# A tag
IMM 1023 
     """,
        ["CP 00 00", "#A tag#IMM 1023"],
        True,
        "",
    ),
    (
        """// this is a line comment that should be ignored
CP 00 12 // some comment
IMM 1253
// Another comment""",
        ["CP 00 12", "IMM 1253"],
        True,
        "",
    ),
    (
        """CP asdasdas gdsgjdskgdjs
IMM 123""",
        [],
        False,
        "line 0",  # check that exception raised contains this
    ),
    (
        """// CP asdasdas gdsgjdskgdjs
IMM 12412512521512
IMM 123""",
        [],
        False,
        "line 1",  # check that exception raised contains this
    ),
    #     ( # let this cook
    #         """CP 00 00
    # # A tag
    # IMM 1023
    # JMP 'A tag'""",
    #         ["CP 00 00", "#A tag#IMM 1023", "JMP 'A tag'"],
    #         True,
    #         "",
    #     ),
]


@pytest.mark.parametrize(
    ("test_code", "expected", "should_pass", "exception_contains"), testdata
)
def test_parsing(
    test_code: str,
    expected: bool,
    should_pass: bool,
    exception_contains: str,
):
    if should_pass:
        assert initial_parse(test_code) == expected
    else:
        with pytest.raises(Exception) as exc_info:
            initial_parse(test_code)
        assert exception_contains in str(exc_info.value).lower()  # type: ignore
